FROM python:3.10.12-slim-bullseye

RUN python3 -m pip --no-cache install datasets transformers[torch] evaluate jiwer soundfile librosa

WORKDIR /app
COPY src/. .

ENTRYPOINT ["python3", "/app/asr.py"]