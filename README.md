# Voice-Feature-Extraction-Toolkit
This repository contains links to repositories that contain example workflows, READMEs, sample data, and [Docker](https://www.docker.com/) files that facilitate the usage of various open-source voice feature extraction packages, tools, datasets, and models.

This toolkit was developed to support scientific research surrounding investigations of relationships between brain aging and voice features, although the extraction of voice features does have wider applicability. We invite others to please offer their questions, ideas, feedback, and improvements on this toolkit.

## Overview
| Name | Description |
| - |-|
| [**2vec**](https://github.com/Digital-Working-Group/audio_embeddings)  | Create audio embeddings via self-supervised learning via [data2vec](https://huggingface.co/docs/transformers/en/model_doc/data2vec) and/or [wav2vec2](https://huggingface.co/docs/transformers/en/model_doc/wav2vec2).
| [**asr**](https://github.com/Digital-Working-Group/automatic_speech_recognition) | Evaluate several automatic speech recognition (ASR) models on different datasets.
| [**diarization-benchmark**](https://github.com/Digital-Working-Group/speaker-diarization) | Evaluate several speaker diarization tools on the [VoxConverse](https://github.com/joonson/voxconverse) dataset.
| [**diarization-pyannote-audio**](https://github.com/Digital-Working-Group/speaker-diarization) | Evaluate the [pyannote-audio](https://github.com/pyannote/pyannote-audio) diarization tool on an audio file.
| [**diarization-whisperx**](https://github.com/Digital-Working-Group/speaker-diarization) | Evaluate ASR via [whisperx](https://github.com/m-bain/whisperX) and optionally align speaker diarization via [pyannote-audio](https://github.com/pyannote/pyannote-audio) on an audio file.
| **espnet** | Evaluate ASR and diarization via the end-to-end Python processing toolkit ([ESPnet](https://github.com/espnet/espnet)) on sample audio files.
| [**example_workflows/standardize**](https://github.com/Digital-Working-Group/example_workflows) | Explore an example of customizable standardization of sample audio data.
| [**example_workflows/standardize_opensmile**](https://github.com/Digital-Working-Group/example_workflows) | Explore an example of customizable standardization and subsequent production of openSMILE acoustic features on sample audio data.
| [**jiwer**](https://github.com/Digital-Working-Group/asr_evaluation) | Evaluate [JiWER](https://github.com/jitsi/jiwer) on sample data, it is a Python package utilized for evaluating ASR systems. It supports the following measures: word error rate (WER), match error rate (MER), word information lost (WIL), word information preserved (WIP), and character error rate (CER).
| **langid** | Evaluate language identification via various models on open-source dataset(s).
| **nlp_features** | Explore examples of the production of natural language processing (NLP) features via several different packages and tools.
| **nltk** | Explore several examples of utilizing the [Natural Language Toolkit (NLTK)](https://github.com/nltk/nltk). NLTK is a suite of open-source Python modules, datasets, and tutorials that support research and development in NLP.
| [**opensmile**](https://github.com/Digital-Working-Group/acoustic_features/) | Explore an example of utilizing [openSMILE](https://www.audeering.com/research/opensmile/) to generate acoustic features. openSMILE is an open-source toolkit for audio analysis especially targeted at speech and music applications (e.g. automatic speech recognition, speaker identification, emotion recognition, etc.).
| **spacy** | Explore several examples of utilizing [spaCy](https://spacy.io/), a Python library for industrial-strength natural language processing, including functionality such as: tokenization, part-of-speech tagging, dependency parsing, lemmatization, sentence boundary location, and named entity recognition.
| **speechbrain** | Explore several examples of utilizing [SpeechBrain](https://speechbrain.github.io/) an open-source PyTorch toolkit for speech and text processing.