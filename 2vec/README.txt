# Project Setup Instructions

## Prerequisites

Ensure you have the following installed:
    Docker Compose

## Step-by-Step Guide

### Step 1: Build the Containers

    Make the build script executable (if not already):

    ```sh
    chmod +x build.sh
    ```

    Run the build script:

    ```sh
    ./build.sh
    ```

    This script will start building the Docker containers required for the project.

### Step 2: Start the Containers with Docker Compose

    Start the containers in detached mode:

    ```sh
    docker-compose up -d
    ```

    This command uses Docker Compose to start all the containers defined in the `docker-compose.yml` file. Running in detached mode means the containers will run in the background.

### Step 3: Monitor and Check Outputs

    The containers will continue to run until they complete their tasks.
    Output files will be sent to the designated output folders as specified in the Docker compose.

### Additional Information

    If you need to stop the containers, you can use:

    ```sh
    docker-compose down
    ```

    Checking Logs: To view the logs of a specific container, you can use:

    ```sh
    docker-compose logs <container_name>
    ```

    Accessing Containers: To access a running container, use:

    ```sh
    docker exec -it <container_name> /bin/bash
    ```

