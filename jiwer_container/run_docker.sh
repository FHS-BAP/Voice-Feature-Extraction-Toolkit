#!/bin/bash

if [ $# -eq 1 ];
then
    container_name=$1
else
    container_name="jiwer-python3"
fi

if [ $# -eq 2 ];
then
    docker_name=$1
else
    docker_name="jiwer-python3"
fi

docker run -v $(pwd):/scripts -it --rm --name $container_name $docker_name bash
