#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
  echo "Container ID not provided." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi
container_id=$1

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Check if speech_separation_example.wav exists in the base directory
if [ ! -f "$BASE_DIR/speech_separation_example.wav" ]; then
  echo "speech_separation_example.wav file not found in $BASE_DIR." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Send a test request to the speech separation endpoint with the audio file
response=$(curl --fail -X POST -F "audio=@$BASE_DIR/speech_separation_example.wav" -o "$BASE_DIR/results/separated_sources.zip" http://localhost:5000/separate_speech)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
  echo "curl command exit status: $?" | tee -a "$BASE_DIR/results/logs.txt"
  echo "Failed to get response from the server." | tee -a "$BASE_DIR/results/logs.txt"
  docker logs $container_id >> "$BASE_DIR/results/logs.txt"
  docker stop $container_id
  docker rm $container_id
  docker rmi speechbrain-demo
  exit 1
fi

# Extract the ZIP archive and save the separated sources as WAV files
unzip -o "$BASE_DIR/results/separated_sources.zip" -d "$BASE_DIR/results/"

# Remove the ZIP archive
rm "$BASE_DIR/results/separated_sources.zip"

echo "Speech separation completed successfully. Separated sources saved in $BASE_DIR/results/." | tee -a "$BASE_DIR/results/logs.txt"