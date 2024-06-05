#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
  echo "Container ID not provided." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi
container_id=$1

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Check if example.wav exists in the base directory
if [ ! -f "$BASE_DIR/example.wav" ]; then
  echo "example.wav file not found in $BASE_DIR." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Send a test request to the voice activity detection endpoint with the audio file
response=$(curl --fail -X POST -F "audio=@$BASE_DIR/example.wav" http://localhost:5000/detect_voice_activity)
echo "Server response: $response" | tee -a "$BASE_DIR/results/logs.txt"

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

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
  echo "Error occurred during voice activity detection:" | tee -a "$BASE_DIR/results/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/results/logs.txt"
  docker logs $container_id >> "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Save the voice activity detection results to a file
echo "$response" > "$BASE_DIR/results/vad_results.txt"

echo "Voice activity detection completed successfully." | tee -a "$BASE_DIR/results/logs.txt"