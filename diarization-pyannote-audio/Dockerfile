FROM python:3.10.12-slim-bullseye

RUN python3 -m pip --no-cache install pyannote.audio

WORKDIR /app
COPY src/. .

ENTRYPOINT diarize.py