Docker container for diarization using [pyannote-audio](https://github.com/pyannote/pyannote-audio)

# Usage
```bash
docker run -it -v <output_volume_name_or_path>:/output <audio_data_volume_or_directory>:/data <image_name> -t <huggingface_token> [-o <output_path>] [-m <model_name>] <audio_path_inside_container>
```

A Huggingface API token is required because you must accept conditions in order to access the model.
1. Accept the terms at https://huggingface.co/pyannote/speaker-diarization-3.1 and https://hf.co/pyannote/segmentation-3.0
2. Create an access token at https://hf.co/settings/tokens
3. Provide the access token when using the container

Default output path is `/output/diaritization-output.rttm` within the container

Default model is [`pyannote/speaker-diarization-3.1`](https://huggingface.co/pyannote/speaker-diarization-3.1)

## Example
To run diarization on the file `./data/audio.wav` writing output to `./output/diaritization-output.rttm`, run
```bash
docker run -it -v ./output:/output ./data:/data <image_name> -t <huggingface_token> /data/audio.wav
```

# Credits
Diarization script based off example in Pyannote-audio's README
