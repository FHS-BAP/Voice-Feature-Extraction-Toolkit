FROM python:3.10.12-slim-bullseye

RUN python3 -m pip --no-cache install \
        pytorch==2.0.0 \
        torchaudio==2.0.0 \
        pytorch-cuda=11.8 \
        git+https://github.com/m-bain/whisperx.git \
        # May not be necessary. Need to test
        openai-whipser \
    && apt update \
    && apt install -y ffmpeg \
    && apt clean

VOLUME /data

ENTRYPOINT /usr/local/bin/whisperx
CMD ["--help"]