#!/bin/bash
if [ $# -eq 1 ];
then
    docker_name=$1
else
    docker_name="standardize_opensmile"
fi
docker build -t $docker_name .
