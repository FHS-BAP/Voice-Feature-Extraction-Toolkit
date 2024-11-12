FROM python:3.10.12-slim-bullseye

RUN --mount=type=cache,target=target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get --no-install-recommends install -y git ffmpeg

RUN --mount=type=cache,target=/root/.cache/pip --mount=source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

VOLUME /data

ENTRYPOINT ["/usr/local/bin/whisperx"]
CMD ["--help"]
