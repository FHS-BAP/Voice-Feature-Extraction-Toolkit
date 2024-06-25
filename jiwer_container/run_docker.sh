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

# data_mnt=/mnt/neuropsych_mnt/filterbanks
# out_mnt=/mnt/neuropsych_mnt/praat_osm/
# docker run -v $scripts:/code -v $data_mnt:$data_mnt -v $out_mnt:$out_mnt -it --rm --gpus all --name $container_name $docker_name bash
docker run -v $scripts:/code -v $data_mnt:$data_mnt -v $landmark_mnt:$landmark_mnt -it --rm --gpus all --name $container_name $docker_name bash
