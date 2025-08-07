# Voice-Feature-Extraction-Toolkit
This repository contains links to repositories that contain example workflows, READMEs, sample data, and [Docker](https://www.docker.com/) files that facilitate the usage of various open-source voice feature extraction packages, tools, datasets, and models.

This toolkit was developed to support scientific research surrounding investigations of relationships between brain aging and voice features, although the extraction of voice features does have wider applicability. We invite others to please offer their questions, ideas, feedback, and improvements on this toolkit.

## Overview
| Name | Description |
| - |-|
| [**2vec**](https://github.com/Digital-Working-Group/audio-embeddings)  | Create audio embeddings via self-supervised learning via [data2vec](https://huggingface.co/docs/transformers/en/model_doc/data2vec) and/or [wav2vec2](https://huggingface.co/docs/transformers/en/model_doc/wav2vec2).
| [**acoustic-features**](https://github.com/Digital-Working-Group/acoustic-features/) | Explore an example of utilizing [openSMILE](https://www.audeering.com/research/opensmile/) to generate acoustic features. openSMILE is an open-source toolkit for audio analysis especially targeted at speech and music applications (e.g. automatic speech recognition, speaker identification, emotion recognition, etc.).
| [**asr**](https://github.com/Digital-Working-Group/automatic-speech-recognition) | Evaluate several automatic speech recognition (ASR) models on different datasets.
| [**speaker-diarization**](https://github.com/Digital-Working-Group/speaker-diarization) | Perform speaker diarization via tools such as [pyannote-audio](https://github.com/pyannote/pyannote-audio) on sample data and datasets such as [VoxConverse](https://github.com/joonson/voxconverse).
| [**jiwer**](https://github.com/Digital-Working-Group/asr-evaluation) | Evaluate [JiWER](https://github.com/jitsi/jiwer) on sample data, it is a Python package utilized for evaluating ASR systems. It supports the following measures: word error rate (WER), match error rate (MER), word information lost (WIL), word information preserved (WIP), and character error rate (CER).
| [**langid**](https://github.com/Digital-Working-Group/language-identification) | Evaluate language identification via various models on open-source dataset(s).
| [**nlp_features**](https://github.com/Digital-Working-Group/natural-language-processing) | Explore examples of the production of natural language processing (NLP) features via several different packages and tools.
| [**voice-standardize**](https://github.com/Digital-Working-Group/voice-standardize) | Standardize digital voice audio files with varying metadata to a standard format using libraries such as [pydub](https://github.com/jiaaro/pydub).