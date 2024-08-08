#!/bin/bash

# Step 1: Make output directory if it does not exist
mkdir -p outputs

# Step 2: Redirect all output to logs.txt, overwriting the previous logs
exec &> >(tee outputs/logs.txt)

# Step 3: Build the Docker image
echo "Building container..."
if docker build -t speechbrain-demo . > /dev/null 2>&1; then
    echo "Build successful."
else
    echo "Failed to build Docker image."
    exit 1
fi

# Step 4: Request port number and start container
while true; do
    echo "Please enter the port number you would like to assign to the Docker container: "
    read port

    if [[ "$port" =~ ^[0-9]+$ ]] && [ "$port" -ge 1 ] && [ "$port" -le 65535 ]; then
        echo "Attempting to start container on port $port..."
        container_id=$(docker run -d -p $port:5000 speechbrain-demo 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "Container started successfully on port $port."
            break
        else
            echo "Failed to start container on port $port. It may be in use."
            echo "Would you like to try another port? (y/n)"
            read response
            if [[ "$response" != "y" ]]; then
                echo "Exiting..."
                exit 1
            fi
        fi
    else
        echo "Invalid input. Please enter a valid port number between 1 and 65535."
    fi
done

# Step 5: Verify container is running
if [ $(docker inspect -f '{{.State.Running}}' $container_id) != "true" ]; then
    echo "Failed to start container."
    docker logs $container_id
    docker stop $container_id
    docker rm $container_id
    docker rmi speechbrain-demo
    exit 1
fi

# Step 6: Wait for container to initialize
echo "Waiting for container to initialize..."
sleep 10
echo "Container is ready."

# Step 7: Get the available functions and implement choice loop

# Set the path to the functions folder
functions_folder="./functions"

# Check if the functions folder exists
if [ ! -d "$functions_folder" ]; then
    echo "Error: Functions folder not found at $functions_folder"
    exit 1
fi

# Get the list of function files
function_files=("$functions_folder"/*.sh)

# Check if any function files were found
if [ ${#function_files[@]} -eq 0 ] || [ ! -e "${function_files[0]}" ]; then
    echo "No function files found in $functions_folder"
    exit 0
fi

# Populate the functions array
functions=()
for file in "${function_files[@]}"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .sh)
        functions+=("$filename")
    fi
done

# Enter a choice loop (functions + exit)
while true; do
    echo "Available functions:"
    for i in "${!functions[@]}"; do
        echo "$((i+1)). ${functions[$i]}"
    done
    exit_option=$((${#functions[@]}+1))
    echo "$exit_option. Exit"

    echo "Enter the number of the function you want to run:"
    read choice

    # Validate input
    if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#functions[@]} ]; then
        selected_function="${functions[$((choice-1))]}"
        echo "Running '$selected_function' function..."
        bash "$functions_folder/$selected_function.sh" $container_id $port
    elif [ "$choice" -eq $exit_option ]; then
        echo "Exiting the program."
        break
    else
        echo "Invalid input. Please enter a number between 1 and $exit_option."
    fi
done

# Append container logs to logs.txt
docker logs $container_id >> outputs/logs.txt

# Clean up
echo "Stopping and removing Docker container..."
docker stop $container_id
docker rm $container_id

echo "Removing Docker image..."
docker rmi speechbrain-demo

echo "Script execution completed."