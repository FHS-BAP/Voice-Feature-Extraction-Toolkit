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

# Request user to insert the relative paths of the input files
echo "Please enter the relative path of the enrollment audio file:"
read enrollment_file
echo "Please enter the relative path of the verification audio file:"
read verification_file

# Check if the input files exist
if [ ! -f "$BASE_DIR/$enrollment_file" ] || [ ! -f "$BASE_DIR/$verification_file" ]; then
  echo "One or both input files not found in $BASE_DIR." | tee -a "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Send a test request to the speaker verification endpoint with the audio files
response=$(curl --fail -X POST -F "enrollment_audio=@$BASE_DIR/$enrollment_file" -F "verification_audio=@$BASE_DIR/$verification_file" http://localhost:$port/verify_speaker)
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
  echo "Error occurred during speaker verification:" | tee -a "$BASE_DIR/outputs/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/outputs/logs.txt"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Save the speaker verification results to a file
echo "$response" > "$BASE_DIR/outputs/speaker_verification_results.txt"

echo "Speaker verification completed successfully."

# Display the speaker verification results
echo "Speaker verification results:"
cat "$BASE_DIR/outputs/speaker_verification_results.txt"

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

# Exit successfully
exit 0