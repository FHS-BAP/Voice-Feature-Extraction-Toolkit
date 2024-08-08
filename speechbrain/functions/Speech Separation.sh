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

# Request user to insert the relative path of the input file
echo "Please enter the relative path of the input audio file for speech separation:"
read input_file

# Check if the input file exists
if [ ! -f "$BASE_DIR/$input_file" ]; then
  echo "Input file not found in $BASE_DIR." | tee -a "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Send a test request to the speech separation endpoint with the audio file
response=$(curl --fail -X POST -F "audio=@$BASE_DIR/$input_file" -o "$BASE_DIR/outputs/separated_sources.zip" http://localhost:$port/separate_speech)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
  echo "curl command exit status: $?" | tee -a "$BASE_DIR/outputs/logs.txt"
  echo "Failed to get response from the server." | tee -a "$BASE_DIR/outputs/logs.txt"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Extract the ZIP archive and save the separated sources as WAV files
unzip -o "$BASE_DIR/outputs/separated_sources.zip" -d "$BASE_DIR/outputs/"

# Remove the ZIP archive
rm "$BASE_DIR/outputs/separated_sources.zip"

echo "Speech separation completed successfully."
echo "Separated sources saved in $BASE_DIR/outputs/."

# List the separated source files
echo "Separated source files:"
ls -1 "$BASE_DIR/outputs/"*.wav

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

# Exit successfully
exit 0