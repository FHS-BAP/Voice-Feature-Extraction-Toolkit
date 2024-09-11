# Example Pipeline for MVP v1.0

This example demonstrates how to use our toolkit to process voice recordings and transcriptions. Follow the steps below to chain various components into a cohesive pipeline.

## Steps

1. **Voice Recordings and/or Manual Transcriptions**: Begin with your raw data.
    a. For this example we use audio files from the AMI corpus dataset.
    b. download.sh downloads the dataset.
    c. input_editor.ipynb moves all the wav files to the input folder. (can delete the amicorpus folder afterwards)
2. **Preprocess Voice Recordings**: Standardize sampling rate, format, bit depth, or bit rate.
    a. this stage was completed within the input_editor notebook using the pydub library.
3. **Language Identification (Optional)**: Detect the language of recordings.
4. **Automatic Speech Recognition (ASR)**: Convert audio to text (verbatim or tailored).
5. **NLP Feature Extraction**: Extract NLP features from transcriptions.


## Selecting Containers
We are going to use some of the pre-built containers to achieve the above steps. For language identification we can use "nltk" container, for ASR we can use speechbrain, for NLP feature extraction we can use "nlp_features" container.


