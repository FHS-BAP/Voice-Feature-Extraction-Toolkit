FROM ubuntu:24.04

# Install Python 3.11, pip, ffmpeg, and jq
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-distutils python3.11-dev python3.11-venv ffmpeg jq && \
    python3.11 -m ensurepip && \
    python3.11 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3.11", "app.py"]