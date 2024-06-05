#!/bin/bash

# Create the results directory if it doesn't exist
mkdir -p results

# Redirect all output to logs.txt, overwriting the previous logs
exec &> >(tee results/logs.txt)

# Build the Docker image
docker build -t spacy-demo .
if [ $? -ne 0 ]; then
    echo "Failed to build Docker image."
    exit 1
fi

# Run the Docker container in detached mode
container_id=$(docker run -d -p 5000:5000 spacy-demo)
if [ $(docker inspect -f '{{.State.Running}}' $container_id) != "true" ]; then
    echo "Failed to start container."
    docker logs $container_id
    exit 1
fi

# Wait for the container to start
sleep 5

# run the subroutines using a for loop
for script in ./subroutines/*_test.sh; do
    bash $script $container_id
    if [ $? -ne 0 ]; then
        exit 1
    fi
done

# Stop and remove the Docker container
docker stop $container_id
docker rm $container_id

# Remove the Docker image
docker rmi spacy-demo