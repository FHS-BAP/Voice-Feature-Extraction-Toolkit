#!/bin/bash

docker build -t grip-dockers/builder:latest -f Dockerfile.builder .
docker build -t grip-dockers/data2vec:latest -f Dockerfile.data2vec . 
docker build -t grip-dockers/wav2vec:latest -f Dockerfile.wav2vec . 