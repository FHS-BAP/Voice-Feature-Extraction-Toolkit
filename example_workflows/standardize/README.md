# standardize_audio.py

> The standardize_audio.py script reads, writes, and standardizes the sample WAV clip.
The scripts can be run with Docker (https://docs.docker.com/engine/install/) or without.

### Sample Input and Output Files

* input_audio/short_wav/first_ten_Sample_HV_Clip.wav
    * a 10-second WAV clip.
* output/
    * write_metadata_to_json/
        * timestamped directories with audio metadata written to JSON files
    * downsampled_wav/downsampled_first_ten_Sample_HV_Clip.wav
        * downsampled version of the WAV clip.

### Install and Run Without Docker

The requirements.txt file can be used to install the necessary libraries without utilizing a Docker environment. Python 3.6.8 was used to develop and test these scripts.
After installing the necessary libraries via requirements.txt:

```sh
pip install -r requirements.txt
python standardize_audio.py
```

### Install and Run With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts and then run extract_features.py within the docker environment.

```sh
./build_docker.sh
./run_docker.sh
python standardize_audio.py
```
