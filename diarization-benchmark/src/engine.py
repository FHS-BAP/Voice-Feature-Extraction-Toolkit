import json
import os
import tempfile
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import *

import boto3
import pvfalcon
import requests
import torch
from google.cloud import speech
from google.cloud import storage
from google.protobuf.json_format import MessageToDict
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment

NUM_THREADS = 1
os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
os.environ["MKL_NUM_THREADS"] = str(NUM_THREADS)
torch.set_num_threads(NUM_THREADS)
torch.set_num_interop_threads(NUM_THREADS)


class Engines(Enum):
    AWS_TRANSCRIBE = "AWS_TRANSCRIBE"
    AZURE_SPEECH_TO_TEXT = "AZURE_SPEECH_TO_TEXT"
    GOOGLE_SPEECH_TO_TEXT = "GOOGLE_SPEECH_TO_TEXT"
    GOOGLE_SPEECH_TO_TEXT_ENHANCED = "GOOGLE_SPEECH_TO_TEXT_ENHANCED"
    PICOVOICE_FALCON = "PICOVOICE_FALCON"
    PYANNOTE = "PYANNOTE"


class Engine:
    def diarization(self, path: str) -> "Annotation":
        raise NotImplementedError()

    def cleanup(self) -> None:
        raise NotImplementedError()

    def is_offline(self) -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    @classmethod
    def create(cls, x: Engines, **kwargs: Any) -> "Engine":
        try:
            subclass = {
                Engines.AWS_TRANSCRIBE: AWSTranscribeEngine,
                Engines.GOOGLE_SPEECH_TO_TEXT: GoogleSpeechToTextEngine,
                Engines.GOOGLE_SPEECH_TO_TEXT_ENHANCED: GoogleSpeechToTextEnhancedEngine,
                Engines.PICOVOICE_FALCON: PicovoiceFalconEngine,
                Engines.PYANNOTE: PyAnnoteEngine,
            }[x]
        except KeyError:
            raise ValueError(f"cannot create `{cls.__name__}` of type `{x.value}`")
        return subclass(**kwargs)


class PicovoiceFalconEngine(Engine):
    def __init__(self, access_key: str) -> None:
        self._falcon = pvfalcon.create(access_key=access_key)
        super().__init__()

    def diarization(self, path: str) -> "Annotation":
        segments = self._falcon.process_file(path)
        return self._segments_to_annotation(segments)

    @staticmethod
    def _segments_to_annotation(segments):
        annotation = Annotation()
        for segment in segments:
            start = segment.start_sec
            end = segment.end_sec
            annotation[Segment(start, end)] = segment.speaker_tag

        return annotation.support()

    def cleanup(self) -> None:
        self._falcon.delete()

    def is_offline(self) -> bool:
        return True

    def __str__(self):
        return Engines.PICOVOICE_FALCON.value


class PyAnnoteEngine(Engine):
    def __init__(self, auth_token: str, use_gpu: bool = False) -> None:
        if use_gpu and torch.cuda.is_available():
            torch_device = torch.device("cuda")
        else:
            torch_device = torch.device("cpu")

        self._pretrained_pipeline = Pipeline.from_pretrained(
            checkpoint_path="pyannote/speaker-diarization-3.1",
            use_auth_token=auth_token,
        )
        self._pretrained_pipeline.to(torch_device)
        super().__init__()

    def diarization(self, path: str) -> "Annotation":
        return self._pretrained_pipeline(path)

    def cleanup(self) -> None:
        self._pretrained_pipeline = None

    def is_offline(self) -> bool:
        return True

    def __str__(self) -> str:
        return Engines.PYANNOTE.value


class AWSTranscribeEngine(Engine):
    def __init__(self, bucket_name: str) -> None:
        self._bucket_name = bucket_name

        self._storage = boto3.client("s3")

        self._transcribe = boto3.client("transcribe")
        super().__init__()

    def diarization(self, path: str) -> "Annotation":
        blob_name = os.path.basename(path)
        temp_path = os.path.join(tempfile.mkdtemp(), blob_name)

        self._storage.upload_file(Filename=path, Bucket=self._bucket_name, Key=blob_name)

        self._transcribe_blob(blob_name=blob_name, results_path=temp_path)

        with open(temp_path) as f:
            transcript = json.load(f)["results"]
        print(transcript)
        return self._transcript_to_annotation(transcript)

    @staticmethod
    def _transcript_to_annotation(transcript: Dict) -> "Annotation":
        segments = transcript["speaker_labels"]["segments"]
        annotation = Annotation()
        for segment in segments:
            start = float(segment["start_time"])
            end = float(segment["end_time"])
            annotation[Segment(start, end)] = segment["speaker_label"]

        return annotation.support()

    def _transcribe_blob(self, blob_name: str, results_path: str) -> None:
        completed = False

        job_name = uuid.uuid4().hex
        response = self._transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode="en-US",
            OutputBucketName=self._bucket_name,
            OutputKey=blob_name + ".json",
            Media={"MediaFileUri": "s3://" + self._bucket_name + "/" + blob_name},
            MediaFormat="wav",
            Settings={
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": 9,
            },
        )

        if response["TranscriptionJob"]["TranscriptionJobStatus"] != "IN_PROGRESS":
            completed = True

        while not completed:
            time.sleep(2)

            response = self._transcribe.get_transcription_job(
                TranscriptionJobName=job_name,
            )

            if response["TranscriptionJob"]["TranscriptionJobStatus"] != "IN_PROGRESS":
                completed = True

        self._storage.download_file(Filename=results_path, Bucket=self._bucket_name, Key=blob_name + ".json")

    def is_offline(self) -> bool:
        return False

    def cleanup(self) -> None:
        pass

    def __str__(self):
        return Engines.AWS_TRANSCRIBE.value


class GoogleSpeechToTextEngine(Engine):
    _diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=1,
        max_speaker_count=20,
    )
    _config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
        diarization_config=_diarization_config,
    )

    def __init__(self, bucket_name: str) -> None:
        self._speech_client = speech.SpeechClient()
        self._storage_client = storage.Client()
        self._bucket_name = bucket_name
        self._bucket = self._storage_client.bucket(bucket_name)

    def diarization(self, path: str) -> "Annotation":
        blob_name = os.path.basename(path)
        self._upload_audio_to_storage(path, blob_name)
        response = self._transcribe_from_storage(path)
        transcript = response["results"]
        return self._transcript_to_annotation(transcript)

    @staticmethod
    def _transcript_to_annotation(transcript: List[Dict]) -> "Annotation":
        words = transcript[-1]["alternatives"][0]["words"]
        annotation = Annotation()
        for word in words:
            start = float(word["startTime"][:-1])
            end = float(word["endTime"][:-1])
            annotation[Segment(start, end)] = word["speakerTag"]

        return annotation.support()

    def _transcribe_from_storage(self, path: str) -> Dict:
        audio = speech.RecognitionAudio(uri=f"gs://{self._bucket_name}/{os.path.basename(path)}")

        operation = self._speech_client.long_running_recognize(config=self._config, audio=audio)
        response = operation.result(timeout=600)
        response_dict = MessageToDict(response._pb)
        return response_dict

    def _upload_audio_to_storage(self, source_file_name: str, blob_name: str) -> None:
        blob = self._bucket.blob(blob_name)
        stats = storage.Blob(bucket=self._bucket, name=blob_name).exists(self._storage_client)
        if not stats:
            blob.upload_from_filename(source_file_name)

    def is_offline(self) -> bool:
        return False

    def cleanup(self) -> None:
        pass

    def __str__(self):
        return Engines.GOOGLE_SPEECH_TO_TEXT.value


class GoogleSpeechToTextEnhancedEngine(GoogleSpeechToTextEngine):
    _diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=1,
        max_speaker_count=20,
    )
    _config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
        diarization_config=_diarization_config,
        model="latest_long",
        use_enhanced=True,
    )

    def __str__(self):
        return Engines.GOOGLE_SPEECH_TO_TEXT_ENHANCED.value
