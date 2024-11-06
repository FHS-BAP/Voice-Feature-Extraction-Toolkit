# standardize_audio.py

> The standardize_audio.py script reads, writes, and standardizes the sample WAV clip.
The script can be run with [Docker](https://docs.docker.com/engine/install/) or without.

### Sample Input and Output Files

* input_audio/short_wav/first_ten_Sample_HV_Clip.wav
    * a 10-second WAV clip.
* output/
    * write_metadata_to_json/
        * timestamped directories with audio metadata written to JSON files
    * downsampled_wav/downsampled_first_ten_Sample_HV_Clip.wav
        * downsampled version of the WAV clip.

### Configuration JSON Files

* config parameters can be changed in the configuration JSON files.
    * **do_write_metadata**:
        * if true, read and write audio metadata from files in **audio_in_root** with extensions included in **audio_in_exts**.
    * **do_downsample**:
        * if true, downsample files to the defined extension (**std_audio_ext**), audio encoding (**std_audio_encoding**), and sampling rate (**std_sampling_rate**).
    * **std_json_in**:
        * if null, search for files to downsample in **audio_in_root**.
        * if set, read this filepath as a JSON to define the audio files to downsample.
    * **std_log_level**:
        * if quiet, then suppress the terminal output from ffmpeg commands.

* config/
    * config.json
        * contains config parameters for reading, writing, and then downsampling of input_audio/ wav files.
    * check_downsample_config.json
        * contains config parameters for reading and writing output/downsampled_wav/ wav files.

### Install FFmpeg

FFMpeg is required to run these scripts and must be available via the command line after installation. Please see the following resources for installation:
* [https://github.com/GyanD/codexffmpeg/releases](https://github.com/GyanD/codexffmpeg/releases)
* [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)

### Install and Run Without Docker

The requirements.txt file can be used to install the necessary libraries without utilizing a Docker environment. Python 3.6.8 was used to develop and test these scripts.

```sh
pip install -r requirements.txt
python standardize_audio.py
```

### Install and Run With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts and then run the script within the docker environment.

```sh
./build_docker.sh
./run_docker.sh
python standardize_audio.py
```
