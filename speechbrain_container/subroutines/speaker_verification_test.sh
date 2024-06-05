#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
  echo "Container ID not provided." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi
container_id=$1

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Check if example.wav and speaker_verification_true.wav exist in the base directory
if [ ! -f "$BASE_DIR/example.wav" ] || [ ! -f "$BASE_DIR/speaker_verification_true.wav" ]; then
  echo "example.wav or speaker_verification_true.wav file not found in $BASE_DIR." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Send a test request to the speaker verification endpoint with the audio files
response=$(curl --fail -X POST -F "enrollment_audio=@$BASE_DIR/example.wav" -F "verification_audio=@$BASE_DIR/speaker_verification_true.wav" http://localhost:5000/verify_speaker)
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
  echo "Error occurred during speaker verification:" | tee -a "$BASE_DIR/results/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/results/logs.txt"
  docker logs $container_id >> "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Save the speaker verification results to a file
echo "$response" > "$BASE_DIR/results/speaker_verification_results.txt"