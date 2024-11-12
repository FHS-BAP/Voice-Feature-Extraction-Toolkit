# espnet
## How to use
transcription_demo.py transcribes the audio.  
    - outputs an output.txt file with the transcription. works well on the test.wav

diarization.py separates an audio file into 2 audio files, each representing one speaker. Note that this requires audio that is single channel.
    It also has a visual output of the spectrograms from each audio file.
    - outputs 2 separate wav files for each speaker, and a visualization of spectrograms for each speaker.

requirements.txt is used to pip install requirements for this to run.

Example Data includes 2 example audio files, one for the transcription (Example Data/test.wav), and one with 2 speakers for diarization (Example Data/Sample_InClinic_Clip_Mono_Short.wav).

Dockerfile is included, simply build (e.g. docker build -t <docker_name> .) and run (e.g. docker run -v $(pwd):/scripts -it --rm --name <container_name> <docker_name> /bin/bash).

Diarization takes a few minutes for a relatively short file.  Transcription takes less than a minute.

When creating container, run from command line so you can run the files within the container. /bin/bash


## Example Usage
### With Docker
- Build Container from directory with dockerfile
    ```
    docker build -t <example_image_name> .
    ```
- Run Docker Image
    ```
    docker run --rm -it <example_image_name>
    ```
- You should now be in the container with a command line that looks like: 
    ```
    root@abcd1234:/espdocker# 
    ```

- Run transcription_demo.py and view output file
    ```
    root@abcd1234:/espdocker# python3 transcription_demo.py
    root@abcd1234:/espdocker# cat output.txt
    ```

- Run diarization
    ```
    root@abcd1234:/espdocker# python3 diarization.py
    ```
    Output is 2 separate audio files in the docker container

- Access audio from docker container
    - Run the following command **external** of the container, where you want the audio stored
        ```
        docker cp container_id:/espdocker/spk1.wav .
        docker cp container_id:/espdocker/spk2.wav .
        ```
        - container_id can be gotten by running
            ```
            hostname
            ```

        within the container
- Other output, like the output.txt can also be copied out of the container if desired:

    ```
    docker cp container_id:/espdocker/output.txt .
    ```
    

### Without Docker
- Install Required Packages
    ```
    pip install -r requirements.txt
    ```

- Run transcription_demo.py and view output file
    ```
    python3 transcription_demo.py
    cat output.txt
    ```

- Run diarization
    ```
    python3 diarization.py
    ```

    - Audio output will be stored in spk1.wav, spk2.wav in working directory


## Acknowledgement
- [espnet](https://github.com/espnet/espnet): End-to-end speech processing toolkit (License Apache)

## Citations
If you use this in your research, please cite this repo:
```bibtex
@misc{fhsbap2024vfetespnetcontainer,
  title={Voice-Feature-Extraction-Toolkit/espnet_container},
  author={Serrano, Xavier},
  journal={GitHub repository},
  year={2024},
  publisher={GitHub},
  howpublished = {\url{https://github.com/FHS-BAP/Voice-Feature-Extraction-Toolkit/tree/main/espnet_container}}
}
```
and these papers:
```bibtex
@inproceedings{watanabe2018espnet,
  author={Shinji Watanabe and Takaaki Hori and Shigeki Karita and Tomoki Hayashi and Jiro Nishitoba and Yuya Unno and Nelson {Enrique Yalta Soplin} and Jahn Heymann and Matthew Wiesner and Nanxin Chen and Adithya Renduchintala and Tsubasa Ochiai},
  title={{ESPnet}: End-to-End Speech Processing Toolkit},
  year={2018},
  booktitle={Proceedings of Interspeech},
  pages={2207--2211},
  doi={10.21437/Interspeech.2018-1456},
  url={http://dx.doi.org/10.21437/Interspeech.2018-1456}
}
@inproceedings{hayashi2020espnet,
  title={{Espnet-TTS}: Unified, reproducible, and integratable open source end-to-end text-to-speech toolkit},
  author={Hayashi, Tomoki and Yamamoto, Ryuichi and Inoue, Katsuki and Yoshimura, Takenori and Watanabe, Shinji and Toda, Tomoki and Takeda, Kazuya and Zhang, Yu and Tan, Xu},
  booktitle={Proceedings of IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages={7654--7658},
  year={2020},
  organization={IEEE}
}
@inproceedings{inaguma-etal-2020-espnet,
    title = "{ESP}net-{ST}: All-in-One Speech Translation Toolkit",
    author = "Inaguma, Hirofumi  and
      Kiyono, Shun  and
      Duh, Kevin  and
      Karita, Shigeki  and
      Yalta, Nelson  and
      Hayashi, Tomoki  and
      Watanabe, Shinji",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-demos.34",
    pages = "302--311",
}
@article{hayashi2021espnet2,
  title={Espnet2-tts: Extending the edge of tts research},
  author={Hayashi, Tomoki and Yamamoto, Ryuichi and Yoshimura, Takenori and Wu, Peter and Shi, Jiatong and Saeki, Takaaki and Ju, Yooncheol and Yasuda, Yusuke and Takamichi, Shinnosuke and Watanabe, Shinji},
  journal={arXiv preprint arXiv:2110.07840},
  year={2021}
}
@inproceedings{li2020espnet,
  title={{ESPnet-SE}: End-to-End Speech Enhancement and Separation Toolkit Designed for {ASR} Integration},
  author={Chenda Li and Jing Shi and Wangyou Zhang and Aswin Shanmugam Subramanian and Xuankai Chang and Naoyuki Kamo and Moto Hira and Tomoki Hayashi and Christoph Boeddeker and Zhuo Chen and Shinji Watanabe},
  booktitle={Proceedings of IEEE Spoken Language Technology Workshop (SLT)},
  pages={785--792},
  year={2021},
  organization={IEEE},
}
@inproceedings{arora2021espnet,
  title={{ESPnet-SLU}: Advancing Spoken Language Understanding through ESPnet},
  author={Arora, Siddhant and Dalmia, Siddharth and Denisov, Pavel and Chang, Xuankai and Ueda, Yushi and Peng, Yifan and Zhang, Yuekai and Kumar, Sujay and Ganesan, Karthik and Yan, Brian and others},
  booktitle={ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages={7167--7171},
  year={2022},
  organization={IEEE}
}
@inproceedings{shi2022muskits,
  author={Shi, Jiatong and Guo, Shuai and Qian, Tao and Huo, Nan and Hayashi, Tomoki and Wu, Yuning and Xu, Frank and Chang, Xuankai and Li, Huazhe and Wu, Peter and Watanabe, Shinji and Jin, Qin},
  title={{Muskits}: an End-to-End Music Processing Toolkit for Singing Voice Synthesis},
  year={2022},
  booktitle={Proceedings of Interspeech},
  pages={4277-4281},
  url={https://www.isca-speech.org/archive/pdfs/interspeech_2022/shi22d_interspeech.pdf}
}
@inproceedings{lu22c_interspeech,
  author={Yen-Ju Lu and Xuankai Chang and Chenda Li and Wangyou Zhang and Samuele Cornell and Zhaoheng Ni and Yoshiki Masuyama and Brian Yan and Robin Scheibler and Zhong-Qiu Wang and Yu Tsao and Yanmin Qian and Shinji Watanabe},
  title={{ESPnet-SE++: Speech Enhancement for Robust Speech Recognition, Translation, and Understanding}},
  year=2022,
  booktitle={Proc. Interspeech 2022},
  pages={5458--5462},
}
@article{gao2022euro,
  title={{EURO}: {ESPnet} Unsupervised ASR Open-source Toolkit},
  author={Gao, Dongji and Shi, Jiatong and Chuang, Shun-Po and Garcia, Leibny Paola and Lee, Hung-yi and Watanabe, Shinji and Khudanpur, Sanjeev},
  journal={arXiv preprint arXiv:2211.17196},
  year={2022}
}
@article{peng2023reproducing,
  title={Reproducing Whisper-Style Training Using an Open-Source Toolkit and Publicly Available Data},
  author={Peng, Yifan and Tian, Jinchuan and Yan, Brian and Berrebbi, Dan and Chang, Xuankai and Li, Xinjian and Shi, Jiatong and Arora, Siddhant and Chen, William and Sharma, Roshan and others},
  journal={arXiv preprint arXiv:2309.13876},
  year={2023}
}
```
