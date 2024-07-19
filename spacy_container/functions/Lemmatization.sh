#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
  echo "Container ID not provided."
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
echo "Please enter the relative path of the input file:"
read input_file

# Check if the input file exists
if [ ! -f "$BASE_DIR/$input_file" ]; then
  echo "Input file not found in $BASE_DIR."
  exit 1
fi

# Read the text from the input file
text=$(cat "$BASE_DIR/$input_file")

# Send a test request to the lemmatization endpoint and save the response
response=$(curl --fail -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"$text\"}" http://localhost:$port/lemmatize)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
  echo "Failed to get response from the server."
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
  echo "Error occurred during lemmatization:"
  echo "$response"
  docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
  exit 1
fi

# Save the lemmatization results to a file
echo "$response" > "$BASE_DIR/outputs/lemmatization_results.txt"

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

echo "Lemmatization completed successfully."

# Display the lemmatization results
echo "Lemmatization results:"
cat "$BASE_DIR/outputs/lemmatization_results.txt"

# Exit successfully
exit 0