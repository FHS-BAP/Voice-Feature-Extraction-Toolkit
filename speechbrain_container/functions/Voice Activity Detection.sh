#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
  echo "Container ID not provided." | tee -a "$BASE_DIR/outputs/logs.txt"
  exit 1
fi
if [ -z "$2" ]; then
  echo "Port not provided." | tee -a "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

container_id=$1
port=$2

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Request user to insert the relative path of the input audio file
echo "Please enter the relative path of the input audio file for voice activity detection:"
read input_file

# Check if the input file exists
if [ ! -f "$BASE_DIR/$input_file" ]; then
  echo "Input file not found in $BASE_DIR." | tee -a "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Send a test request to the voice activity detection endpoint with the audio file
response=$(curl --fail -X POST -F "audio=@$BASE_DIR/$input_file" http://localhost:$port/detect_voice_activity)
echo "Server response: $response" | tee -a "$BASE_DIR/outputs/logs.txt"

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
  echo "curl command exit status: $?" | tee -a "$BASE_DIR/outputs/logs.txt"
  echo "Failed to get response from the server." | tee -a "$BASE_DIR/outputs/logs.txt"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
  echo "Error occurred during voice activity detection:" | tee -a "$BASE_DIR/outputs/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/outputs/logs.txt"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Save the voice activity detection results to a file
echo "$response" > "$BASE_DIR/outputs/vad_results.txt"

echo "Voice activity detection completed successfully."

# Display the voice activity detection results
echo "Voice activity detection results:"
cat "$BASE_DIR/outputs/vad_results.txt"

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

# Exit successfully
exit 0