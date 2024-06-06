import soundfile
import numpy as np
import os
import tqdm
import torch

def process_files(audio_files, INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH, processor, model):
    for file_name in tqdm.tqdm(audio_files):
        # Read the WAV file
        file_path = os.path.join(INPUT_FOLDER_PATH, file_name)
        try:
            data, samplerate = soundfile.read(file_path)
        except soundfile.LibsndfileError:
            print('Unknown error with libsndfile')
            continue
        ds = np.array(data)
        input_values = processor(ds, return_tensors="pt", padding="longest",
                                sampling_rate=16000).input_values  # Batch size 1

        logits = model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)
        file_name, _ = os.path.splitext(file_name)
        output_file_path = os.path.join(
            OUTPUT_FOLDER_PATH, file_name + '.txt')
        with open(output_file_path, 'w') as f:
            f.write(transcription[0])