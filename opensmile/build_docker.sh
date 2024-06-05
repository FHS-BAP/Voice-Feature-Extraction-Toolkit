#!/bin/bash
if [ $# -eq 1 ];
then
    docker_name=$1
else
    docker_name="osm-feat-rhel8-python3"
fi
docker build -t $docker_name .
