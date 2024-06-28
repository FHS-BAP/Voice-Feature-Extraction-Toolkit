transcription_demo.py transcribes the audio.  
    - outputs an output.txt file with the transcription. works well on the test.wav

diarization.py separates an audio file into 2 audio files, each representing one speaker. Note that this requires audio that is single channel.
    It also has a visual output of the spectrograms from each audio file.
    - outputs 2 separate wav files for each speaker, and a visualization of spectrograms for each speaker.

requirements.txt is used to pip install requirements for this to run.

Example Data includes 2 example audio files, one for the transcription (Example Data/test.wav), and one with 2 speakers for diarization (Example Data/Sample_InClinic_Clip_Mono_Short.wav).

Dockerfile is included, simply build and run.  Diarization takes a few minutes for a relatively short file.  Transcription takes less than a minute.

When creating container, run from command line so you can run the files within the container. /bin/bash