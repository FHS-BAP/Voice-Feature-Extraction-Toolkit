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

# Request user to insert the relative path of the first input file
echo "Please enter the relative path of the first input file:"
read input_file1

# Request user to insert the relative path of the second input file
echo "Please enter the relative path of the second input file:"
read input_file2

# Check if both input files exist
if [ ! -f "$BASE_DIR/$input_file1" ] || [ ! -f "$BASE_DIR/$input_file2" ]; then
    echo "One or both input files not found in $BASE_DIR."
    exit 1
fi

# Read the text from both input files
text1=$(cat "$BASE_DIR/$input_file1")
text2=$(cat "$BASE_DIR/$input_file2")

# Send a test request to the text similarity endpoint and save the response
response=$(curl --fail -s -X POST -H "Content-Type: application/json" -d "{\"text1\": \"$text1\", \"text2\": \"$text2\"}" http://localhost:$port/text_similarity)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
    echo "Failed to get response from the server."
    docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
    exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
    echo "Error occurred during text similarity calculation:"
    echo "$response"
    docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
    exit 1
fi

# Save the text similarity results to a file
echo "$response" > "$BASE_DIR/outputs/text_similarity_results.txt"

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

echo "Text similarity calculation completed successfully."

# Display the text similarity results
echo "Text similarity results:"
cat "$BASE_DIR/outputs/text_similarity_results.txt"

# Exit successfully
exit 0