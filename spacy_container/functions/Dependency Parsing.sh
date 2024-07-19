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

# print port
echo "Port: $port" | tee -a "$BASE_DIR/outputs/logs.txt"

# Send a test request to the tokenization endpoint and save the response
response=$(curl --fail -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"$text\"}" http://localhost:$port/dep_parse)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
    echo "Failed to get response from the server."
    docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
    exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
    echo "Error occurred during dependency parsing:"
    echo "$response"
    docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
    exit 1
fi

# Save the dependency parsing results to a file
echo "$response" > "$BASE_DIR/outputs/dep_parsing_results.txt"

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

echo "Dependency parsing completed successfully."

# Display the dependency parsing results
echo "Dependency parsing results:"
cat "$BASE_DIR/outputs/dep_parsing_results.txt"

# Exit successfully
exit 0