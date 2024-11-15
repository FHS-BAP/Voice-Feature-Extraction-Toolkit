FROM python:3.10.12-slim-bullseye

WORKDIR /app/
COPY ./src/. .

RUN mkdir -p /data/voxconverse/wav/dev /data/voxconverse/wav/test /data/voxconverse/labels/

# Install git
RUN --mount=type=cache,target=target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get --no-install-recommends install -y git

# Download VoxConverse data
ADD https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_dev_wav.zip /data/voxconverse/dev/
ADD https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_test_wav.zip /data/voxconverse/test/

# Download VoxConverse labels
RUN git clone --depth=1 https://github.com/joonson/voxconverse.git /data/voxconverse/labels/

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt --mount=type=cache,target=/root/.cache pip install -r /tmp/requirements.txt

ENTRYPOINT ["python3", "/app/benchmark.py"]
