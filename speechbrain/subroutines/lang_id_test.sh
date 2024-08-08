#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
  echo "Container ID not provided." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi
if [ -z "$2" ]; then
  echo "Port not provided." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi

container_id=$1
port=$2

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Check if example.wav exists in the base directory
if [ ! -f "$BASE_DIR/example.wav" ]; then
  echo "example.wav file not found in $BASE_DIR." | tee -a "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Send a test request to the language identification endpoint with the audio file
response=$(curl --fail -X POST -F "audio=@$BASE_DIR/example.wav" http://localhost:$port/identify_language)
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
  echo "Error occurred during language identification:" | tee -a "$BASE_DIR/results/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/results/logs.txt"
  docker logs $container_id >> "$BASE_DIR/results/logs.txt"
  exit 1
fi

# Save the language identification results to a file
echo "$response" > "$BASE_DIR/results/language_identification_results.txt"

# Extract the predicted language and likelihood from the response
predicted_language=$(echo "$response" | grep -o '"language":"[^"]*"' | sed 's/"language":"//;s/"//')
likelihood=$(echo "$response" | grep -o '"likelihood":[0-9.]*' | sed 's/"likelihood"://')

# Check if the predicted language and likelihood are valid
if [ -z "$predicted_language" ] || [ -z "$likelihood" ]; then
  echo "Invalid language identification results:" | tee -a "$BASE_DIR/results/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/results/logs.txt"
  docker logs $container_id >> "$BASE_DIR/results/logs.txt"
  exit 1
fi

echo "Language identification completed successfully." | tee -a "$BASE_DIR/results/logs.txt"
echo "Predicted language: $predicted_language" | tee -a "$BASE_DIR/results/logs.txt"
echo "Likelihood: $likelihood" | tee -a "$BASE_DIR/results/logs.txt"