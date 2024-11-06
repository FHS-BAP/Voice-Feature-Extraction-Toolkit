# standardize_opensmile.py

> The standardize_opensmile.py script standardizes the sample WAV clip and then produces openSMILE acoustic features. The script can be run with [Docker](https://docs.docker.com/engine/install/) or without.

### Sample Input and Output Files

* input_audio/short_wav/first_ten_Sample_HV_Clip.wav
    * a 10-second WAV clip.
* output/
    * downsampled_wav/downsampled_first_ten_Sample_HV_Clip.wav
        * downsampled version of the WAV clip.
    * osm/
        * downsampled_first_ten_Sample_HV_Clip_lld.csv
            * LLD features generated from the downsampled WAV clip.
        * downsampled_first_ten_Sample_HV_Clip_functionals.csv
            * Functionals features generated from the downsampled WAV clip.

### Configuration JSON Files

* config parameters can be changed in the configuration JSON files.
    * **do_downsample**:
        * if true, downsample files in **audio_in_root** to the defined extension (**std_audio_ext**), audio encoding (**std_audio_encoding**), and sampling rate (**std_sampling_rate**).
    * **std_log_level**:
        * if quiet, then suppress the terminal output from ffmpeg commands.
    * **osm_feat_list**:
        * list of openSMILE features to generate.
            * if files are downsampled (do_downsample=True), then it iterates over the downsampled files.
            * otherwise, it iterates over audio files in **audio_in_root**.
* config/config.json
    * contains config parameters for reading, writing, and then downsampling of input_audio/ wav files.

### Install FFmpeg

FFMpeg is required to run these scripts and must be available via the command line after installation. Please see the following resources for installation:
* [https://github.com/GyanD/codexffmpeg/releases](https://github.com/GyanD/codexffmpeg/releases)
* [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)

### Install and Run Without Docker

The requirements.txt file can be used to install the necessary libraries without utilizing a Docker environment. Python 3.12.3 was used to develop and test these scripts.

```sh
pip install -r requirements.txt
python standardize_opensmile.py
```

### Install and Run With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts and then run the script within the docker environment.

```sh
./build_docker.sh
./run_docker.sh
python standardize_opensmile.py
```
## Acknowledgement
- [openSMILE](https://github.com/audeering/opensmile): Open-source Speech and Music Interpretation by Large-space Extraction (License audEERING GmbH)

## Citations
```bibtex
@article{eyben2010opensmile,
  title={openSMILE - The Munich Versatile and Fast Open-Source Audio Feature Extractor},
  author={Eyben, Florian and Wöllmer, Martin and Schuller, Björn},
  booktitle={Proc. ACM Multimedia (MM)},
  organization={ACM},
  address={Florence, Italy},
  isbn={978-1-60558-933-6},
  pages={1459-1462},
  year={2010}
}
```
