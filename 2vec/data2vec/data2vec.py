from transformers import Wav2Vec2Processor, Data2VecAudioForCTC
import torch
import soundfile
import numpy as np
import os
from utils import process_files
INPUT_FOLDER_PATH = os.environ.get('AUDIO_INPUT')
OUTPUT_FOLDER_PATH = os.environ.get('AUDIO_OUTPUT')

# Ensure the output folder exists, create if not
if not os.path.exists(OUTPUT_FOLDER_PATH):
    os.makedirs(OUTPUT_FOLDER_PATH)

processor = Wav2Vec2Processor.from_pretrained(
    "facebook/data2vec-audio-base-100h")
model = Data2VecAudioForCTC.from_pretrained(
    "facebook/data2vec-audio-base-100h")

# Get list of WAV files in input folder
audio_files = [f for f in os.listdir(INPUT_FOLDER_PATH) if f.endswith('.wav') or f.endswith('.flac')]

# Process each WAV file
process_files.process_files(audio_files, INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH, processor, model)
