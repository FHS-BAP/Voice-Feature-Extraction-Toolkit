FROM python:3.10.12-slim-bullseye

RUN git clone --depth=1 https://github.com/MahmoudAshraf97/whisper-diarization.git /app

WORKDIR /app
RUN python3 -m pip --no-cache install cython \
    && python3 -m pip --no-cache install -r requirements \
    && apt update \
    && apt install ffmpeg

ENTRYPOINT diarize.py