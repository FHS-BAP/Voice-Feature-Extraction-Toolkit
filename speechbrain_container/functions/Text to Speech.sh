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

# Request user to insert the relative path of the input text file
echo "Please enter the relative path of the input text file for text-to-speech:"
read input_file

# Check if the input file exists
if [ ! -f "$BASE_DIR/$input_file" ]; then
  echo "Input file not found in $BASE_DIR." | tee -a "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Send a test request to the text-to-speech endpoint with the text file
response=$(curl --fail -X POST -F "text=@$BASE_DIR/$input_file" -o "$BASE_DIR/outputs/tts_result.wav" http://localhost:$port/text_to_speech)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
  echo "curl command exit status: $?" | tee -a "$BASE_DIR/outputs/logs.txt"
  echo "Failed to get response from the server." | tee -a "$BASE_DIR/outputs/logs.txt"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

echo "Text-to-speech completed successfully."
echo "Generated audio saved in $BASE_DIR/outputs/tts_result.wav."

# Verify the generated audio file exists
if [ -f "$BASE_DIR/outputs/tts_result.wav" ]; then
  echo "Generated audio file details:"
  ls -lh "$BASE_DIR/outputs/tts_result.wav"
else
  echo "Warning: Generated audio file not found." | tee -a "$BASE_DIR/outputs/logs.txt"
fi

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

# Exit successfully
exit 0