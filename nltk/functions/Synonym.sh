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

# Request user to enter a word for synonym lookup
echo "Please enter a word to find synonyms for:"
read word

# Send a test request to the synonyms endpoint and save the response
response=$(curl --fail -s -X POST -H "Content-Type: application/json" -d "{\"word\": \"$word\"}" http://localhost:$port/synonyms)

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
    echo "Failed to get response from the server."
    docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
    exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
    echo "Error occurred while finding synonyms:"
    echo "$response"
    docker logs $container_id >> "$BASE_DIR/outputs/logs.txt"
    exit 1
fi

# Save the synonyms results to a file
echo "$response" > "$BASE_DIR/outputs/synonyms_results.txt"

# Append container logs to logs.txt without writing to stdout
#docker logs $container_id >> "$BASE_DIR/outputs/logs.txt" 2>&1

echo "Synonym lookup completed successfully."

# Display the synonyms results
echo "Synonyms results:"
cat "$BASE_DIR/outputs/synonyms_results.txt"

# Exit successfully
exit 0