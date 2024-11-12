# Voice-Feature-Extraction-Toolkit
This repository contains READMEs, sample data, and Docker containers to facilitate the usage of various open-source voice feature extraction packages, tools, datasets, and models.
## Overview
| Name | Description |
| - |-|
| **2vec**  | Create audio embeddings via self-supervised learning via [data2vec](https://huggingface.co/docs/transformers/en/model_doc/data2vec) and/or [wav2vec2]((https://huggingface.co/docs/transformers/en/model_doc/wav2vec2).
| **asr** | Evaluate several automatic speech recognition models on different datasets.
| **diarization-benchmark** | Evaluate several speaker diarization tools on the [VoxConverse](https://github.com/joonson/voxconverse) dataset.
| **diarization-pyannote-audio** | Evaluate the [pyannote-audio](https://github.com/pyannote/pyannote-audio) diarization tool on an audio file.
| **diarization-whisperx** | Evaluate ASR via [whisperx](https://github.com/m-bain/whisperX) and optionally align speaker diarization via [pyannote-audio](https://github.com/pyannote/pyannote-audio) on an audio file.
| **espnet** | Evaluate ASR and diarization via the end-to-end Python processing toolkit ([ESPnet](https://github.com/espnet/espnet)) on sample audio files.
| **JiWER** | Evaluate [JiWER](https://github.com/jitsi/jiwer) on sample data, it is a Python package utilized for evaluating ASR systems. It supports the following measures: word error rate (WER), match error rate (MER), word information lost (WIL), word information preserved (WIP), and character error rate (CER).
## langid
Evaluate language identification models on datasets
## nltk
NLTK is a suite of open source Python modules, data sets, and tutorials supporting research and development in natural language processing.
## opensmile
openSMILE (open-source Speech and Music Interpretation by Large-space Extraction) is an open-source toolkit for audio analysis especially targeted at speech and music applications (e.g. automatic speech recognition, speaker identification, emotion recognition, etc.).
## spacy
spaCy is a Python library for industrial-strength natural language processing, including functionality such as: tokenization, part-of-speech tagging, dependency parsing, lemmatization, sentence boundary location, and named entity recognition.
## speechbrain
SpeechBrain is an open-source PyTorch toolkit for speech and text processing.