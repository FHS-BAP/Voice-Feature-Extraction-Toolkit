#!/bin/bash

# Ensure the script has received the container ID as a parameter
if [ -z "$1" ]; then
    echo "Container ID not provided."
    exit 1
fi

container_id=$1

# Set the base directory relative to the script's location
BASE_DIR=$(dirname "$0")/..

# Check if example.txt and example_2.txt exist in the base directory
if [ ! -f "$BASE_DIR/example.txt" ] || [ ! -f "$BASE_DIR/example_2.txt" ]; then
    echo "example.txt or example_2.txt file not found in $BASE_DIR."
    exit 1
fi

# Send a test request to the text similarity endpoint and save the response
response=$(curl --fail -s -X POST http://localhost:5000/text_similarity)

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
    echo "Error occurred during text similarity calculation:"
    echo "$response"
    docker logs $container_id >> "$BASE_DIR/results/logs.txt"
    docker stop $container_id
    docker rm $container_id
    docker rmi nltk-demo
    exit 1
fi

# Save the text similarity results to a file
echo "$response" > "$BASE_DIR/results/text_similarity_results.txt"

# Append container logs to logs.txt
docker logs $container_id >> "$BASE_DIR/results/logs.txt"