#!/bin/bash

# Set default port value
PORT=5000

# read port flag
# Parse command line options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--port) PORT="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "Using port $PORT"

# Create the results directory if it doesn't exist
mkdir -p results

# Redirect all output to logs.txt, overwriting the previous logs
exec &> >(tee results/logs.txt)

# Build the Docker image
docker build -t speechbrain-demo .
if [ $? -ne 0 ]; then
    echo "Failed to build Docker image."
    exit 1
fi

# Run the Docker container in detached mode
container_id=$(docker run -d -p $PORT:5000 speechbrain-demo)
if [ $(docker inspect -f '{{.State.Running}}' $container_id) != "true" ]; then
    echo "Failed to start container."
    docker logs $container_id
    exit 1
fi

# Wait for the container to start
sleep 10

# Wait for the container to be ready
# echo "Waiting for the container to be ready..."
# while ! docker exec $container_id curl -s --head http://localhost:5000 >/dev/null; do
#     sleep 1
# done
# echo "Container is ready."

# run the subroutines using a for loop
for script in ./subroutines/*_test.sh; do
    bash $script $container_id $PORT
    if [ $? -ne 0 ]; then
        # break the loop if a script fails
        echo "Failed to run $script"
        break
    fi
done

# Append container logs to logs.txt
docker logs $container_id >> results/logs.txt

# Stop and remove the Docker container
docker stop $container_id
docker rm $container_id

# Remove the Docker image
docker rmi speechbrain-demo