FROM python:3.10.12-slim-bullseye

RUN --mount=type=cache,target=/root/.cache/pip --mount=source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

WORKDIR /app
COPY src/. .

ENTRYPOINT ["python3", "/app/diarize.py"]
