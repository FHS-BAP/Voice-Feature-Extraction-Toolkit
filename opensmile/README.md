# openSMILE Docker Examples

> Examples of using the openSMILE Python library without and with [Docker.](https://docs.docker.com/engine/install/)

This repository contains scripts that show examples of how to use the [openSMILE Python library](https://audeering.github.io/opensmile-python/) to generate Low Level Descriptors (LLDs) and Functionals from the ComParE 2016 feature set. The scripts can be run without and with Docker.

## Installation

### Without Docker

The requirements.txt file can be used to install the necessary libraries without utilizing a Docker environment. Python 3.9.18 was used to develop and test these scripts.

```sh
pip install -r requirements.txt
```

### With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

## Usage example

The extract_features.py script generates both LLDs and functionals on the provided sample WAV file.

### Sample Input and Output Files

* Sample Input: 
    * sample_wav/
        * first_ten_Sample_HV_Clip.wav contains a 10-second WAV clip.
* Sample Output:
    * sample_out/
        * first_ten_Sample_HV_Clip_lld.csv
        * first_ten_Sample_HV_Clip_functionals.csv

### Without Docker

After installing the necessary libraries via requirements.txt:

```sh
python extract_features.py
```

### With Docker

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts and then run extract_features.py within the docker environment.

```sh
./build_docker.sh
./run_docker.sh
python3 extract_features.py
```