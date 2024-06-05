#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
  echo "Container ID not provided." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi
container_id=$1

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Check if tts_example.txt exists in the base directory
if [ ! -f "$BASE_DIR/example_tts.txt" ]; then
  echo "example_tts.txt file not found in $BASE_DIR." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Send a test request to the text-to-speech endpoint with the text file
response=$(curl --fail -X POST -F "text=@$BASE_DIR/example_tts.txt" -o "$BASE_DIR/results/tts_result.wav" http://localhost:5000/text_to_speech)

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

echo "Text-to-speech completed successfully. Generated audio saved in $BASE_DIR/results/tts_result.wav." | tee -a "$BASE_DIR/results/logs.txt"