FROM ubuntu:24.04

## ffmpeg installation comes with python3.12
RUN apt-get update && apt-get install -y ffmpeg && \
    apt-get install -y python3.12-venv && \
    python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /scripts
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
