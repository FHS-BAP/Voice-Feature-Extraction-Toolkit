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

# Request max_ngram value from the user
echo "Please enter the max_ngram value (default is 3):"
read max_ngram
max_ngram=${max_ngram:-3}

# Send a request to the ngram_repetition endpoint and save the response
response=$(curl --fail -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"$text\", \"max_ngram\": $max_ngram}" http://localhost:$port/ngram_repetition)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
    echo "Failed to get response from the server."
    docker logs $container_id >> "$BASE_DIR/output/logs.txt"
    exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
    echo "Error occurred while finding ngram repetitions:"
    echo "$response"
    docker logs $container_id >> "$BASE_DIR/output/logs.txt"
    exit 1
fi

# Save the ngram repetition results to a file
echo "$response" > "$BASE_DIR/output/ngram_repetition_results.json"

echo "N-gram repetition analysis completed successfully."

# Display the ngram repetition results
echo "N-gram repetition results:"
cat "$BASE_DIR/output/ngram_repetition_results.json"

# Exit successfully
exit 0