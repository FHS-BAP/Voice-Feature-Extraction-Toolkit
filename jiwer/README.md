# JiWER Docker Examples

> Examples of using the JiWER Python library with and without [Docker.](https://docs.docker.com/engine/install/)

This repository contains scripts that show examples of how to use the [JiWER Python library](https://github.com/jitsi/jiwer) to evaluate the effectiveness of automatic speech transcription software. The scripts can be run with and without Docker.

## Installation

### Without Docker

The following command can be used to install the necessary libraries without utilizing a Docker environment. Python 3.9.18 was used to develop and test these scripts.

```sh
pip install -r requirements.txt
```

### With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

## Usage example

The jiwer_example.py script generates the word error rate (WER), match error rate (MER), word information lost (WIL), word information preserved (WIP), character error rate (CER) metrics of auto_transcript.txt compared to manual_transcript.txt

### Sample Input and Output Files

* Sample Input: 
    * auto_transcript.txt
        * contains an automatic transcription of a short audio clip
    * manual_transcript.txt
        * contains a manual transcription of the same audio clip to compare the automation to
* Sample Output:
    * prints the described metrics to the console

### Without Docker

After installing the necessary libraries via requirements.txt:

```sh
python jiwer_example.py
```

### With Docker

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts and then run extract_features.py within the docker environment.

```sh
./build_docker.sh
./run_docker.sh
python3 jiwer_example.py
```

## Acknowledgement
- [jiwer](https://github.com/jitsi/jiwer): Simple and fast python package to evaluate an automatic speech recognition system (License Apache)

## Citations
If you use this in your research, please cite this repo:
```bibtex
@misc{fhsbap2024vfetjiwercontainer,
  title={Voice-Feature-Extraction-Toolkit/jiwer_container},
  author={Peterson, Julia},
  journal={GitHub repository},
  year={2024},
  publisher={GitHub},
  howpublished = {\url{https://github.com/FHS-BAP/Voice-Feature-Extraction-Toolkit/tree/main/jiwer_container}}
}
```
