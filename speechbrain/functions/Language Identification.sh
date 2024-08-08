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
echo "Please enter the relative path of the input audio file:"
read input_file

# Check if the input file exists
if [ ! -f "$BASE_DIR/$input_file" ]; then
  echo "Input file not found in $BASE_DIR." | tee -a "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Send a test request to the language identification endpoint with the audio file
response=$(curl --fail -X POST -F "audio=@$BASE_DIR/$input_file" http://localhost:$port/identify_language)
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
  echo "Error occurred during language identification:" | tee -a "$BASE_DIR/outputs/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/outputs/logs.txt"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Save the language identification results to a file
echo "$response" > "$BASE_DIR/outputs/language_identification_results.txt"

# Extract the predicted language and likelihood from the response
predicted_language=$(echo "$response" | grep -o '"language":"[^"]*"' | sed 's/"language":"//;s/"//')
likelihood=$(echo "$response" | grep -o '"likelihood":[0-9.]*' | sed 's/"likelihood"://')

# Check if the predicted language and likelihood are valid
if [ -z "$predicted_language" ] || [ -z "$likelihood" ]; then
  echo "Invalid language identification results:" | tee -a "$BASE_DIR/outputs/logs.txt"
  echo "$response" | tee -a "$BASE_DIR/outputs/logs.txt"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

echo "Language identification completed successfully."
echo "Predicted language: $predicted_language"
echo "Likelihood: $likelihood"

# Display the language identification results
echo "Language identification results:"
cat "$BASE_DIR/outputs/language_identification_results.txt"

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

# Exit successfully
exit 0