#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
    echo "Container ID not provided."
    exit 1
fi

container_id=$1

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Check if example.txt exists in the base directory
if [ ! -f "$BASE_DIR/example.txt" ]; then
    echo "example.txt file not found in $BASE_DIR."
    exit 1
fi

# Read the text from example.txt
text=$(cat "$BASE_DIR/example.txt")

# Send a test request to the lemmatization endpoint and save the response
response=$(curl --fail -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"$text\"}" http://localhost:5000/lemmatize)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
    echo "Failed to get response from the server."
    docker logs $container_id >> "$BASE_DIR/results/logs.txt"
    docker stop $container_id
    docker rm $container_id
    docker rmi nltk-demo
    exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
    echo "Error occurred during lemmatization:"
    echo "$response"
    docker logs $container_id >> "$BASE_DIR/results/logs.txt"
    docker stop $container_id
    docker rm $container_id
    docker rmi nltk-demo
    exit 1
fi

# Save the lemmatization results to a file
echo "$response" > "$BASE_DIR/results/lemmatize_results.txt"

# Append container logs to logs.txt
docker logs $container_id >> "$BASE_DIR/results/logs.txt"