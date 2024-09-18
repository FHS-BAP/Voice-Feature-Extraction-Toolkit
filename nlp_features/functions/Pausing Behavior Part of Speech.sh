#!/bin/bash

# Ensure the script has received the container ID and port as parameters
if [ -z "$1" ]; then
    echo "Container ID not provided."
    exit 1
fi
if [ -z "$2" ]; then
    echo "Port not provided."
    exit 1
fi

container_id=$1
port=$2

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Request user to insert the relative path of the input audio file
echo "Please enter the relative path of the input audio file (supported formats: wav, mp3, m4a, mp4, ogg, flac):"
read input_file

# Check if the input file exists
if [ ! -f "$BASE_DIR/$input_file" ]; then
    echo "Input file not found in $BASE_DIR."
    exit 1
fi

# Get the file extension
file_extension="${input_file##*.}"
file_extension=$(echo "$file_extension" | tr '[:upper:]' '[:lower:]')

# Check if the file type is supported
if [[ ! "$file_extension" =~ ^(wav|mp3|m4a|mp4|ogg|flac)$ ]]; then
    echo "Unsupported file type: $file_extension"
    echo "Supported formats are: wav, mp3, m4a, mp4, ogg, flac"
    exit 1
fi

# Send a request to the pausing_behavior endpoint and save the response
response=$(curl --fail -s -X POST -H "Content-Type: application/json" -d "{\"audio_path\": \"$BASE_DIR/$input_file\"}" http://localhost:$port/pausing_behavior)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
    echo "Failed to get response from the server."
    docker logs $container_id >> "$BASE_DIR/output/logs.txt"
    exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
    echo "Error occurred while calculating Pausing Behavior:"
    echo "$response"
    docker logs $container_id >> "$BASE_DIR/output/logs.txt"
    exit 1
fi

# Save the Pausing Behavior results to a file
echo "$response" > "$BASE_DIR/output/pausing_behavior_results.json"

echo "Pausing Behavior calculation completed successfully."

# Display the Pausing Behavior results
echo "Pausing Behavior results:"
cat "$BASE_DIR/output/pausing_behavior_results.json"

# Exit successfully
exit 0