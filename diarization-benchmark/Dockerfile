FROM python:3.10.12-slim-bullseye

WORKDIR /app/

RUN mkdir -p /data/voxconverse/wav/dev /data/voxconverse/wav/test /data/voxconverse/labels/

ADD https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_dev_wav.zip /data/voxconverse/dev/
ADD https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_test_wav.zip /data/voxconverse/test/

RUN git clone --depth=1 https://github.com/joonson/voxconverse.git /data/voxconverse/labels/

RUN git clone --depth=1 https://github.com/Picovoice/speaker-diarization-benchmark.git /app/

# TODO: Verify cache directory
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt --mount=type=cache,target=/root/.cache pip install -r /tmp/requirements.txt

ENTRYPOINT ["/app/benchmark.py"]