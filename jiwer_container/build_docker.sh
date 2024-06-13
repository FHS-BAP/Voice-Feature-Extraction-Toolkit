#!/bin/bash
if [ $# -eq 1 ];
then
	docker_name=$1
else
	docker_name="jiwer-python3"
fi
docker build -t $docker_name .
