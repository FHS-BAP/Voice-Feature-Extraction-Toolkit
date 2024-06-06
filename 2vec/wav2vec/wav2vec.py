from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import torch
import soundfile
import numpy as np
import os
from utils import process_files
INPUT_FOLDER_PATH = os.environ.get('AUDIO_INPUT')
OUTPUT_FOLDER_PATH = os.environ.get('AUDIO_OUTPUT')
# load model and tokenizer
processor = Wav2Vec2Processor.from_pretrained(
    "facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
# load dummy dataset and read soundfiles


# Get list of WAV files in input folder
audio_files = [f for f in os.listdir(INPUT_FOLDER_PATH) if f.endswith('.wav') or f.endswith('.flac')]

# Process each WAV file
process_files.process_files(audio_files, INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH, processor, model)