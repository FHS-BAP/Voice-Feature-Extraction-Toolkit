# SpeechBrain

## Supported Tasks

- Speech Recognition
- Speaker Recognition
- Speech Separation
- Speech Enhancement
- Text-to-Speech
- Vocoding
- Spoken Language Understanding
- Speech-to-Speech Translation
- Speech Translation
- Emotion Classification
- Language Identification
- Voice Activity Detection
- Sound Classification
- Self-Supervised Learning
- Interpretabiliy
- Speech Generation
- Metric Learning
- Allignment
- Diarization
- Language Modeling
- Response Generation
- Grapheme-to-Phoneme

## How to use

cd into this directory and run the following command:

```bash
./test.sh
```

It will setup the docker container, and iterate through the subroutines to demonstrate the functionalities.

## Updating subroutines

For customizing the inputs, you would need to upload your files of interest, and updates the subroutines to target them.

## Acknowledgement
- [SpeechBrain](https://github.com/speechbrain/speechbrain): Open-source PyTorch toolkit that accelerates Conversational AI development (License Apache)

## Citations
If you use this in your research, please cite this repo:
```bibtex
@misc{fhsbap2024vfetspeechbraincontainer,
  title={Voice-Feature-Extraction-Toolkit/speechbrain_container},
  author={Khemakhem, Mahdi},
  journal={GitHub repository},
  year={2024},
  publisher={GitHub},
  howpublished = {\url{https://github.com/FHS-BAP/Voice-Feature-Extraction-Toolkit/tree/main/speechbrain_container}}
}
```
and the SpeechBrain paper:
```bibtex
@misc{speechbrain,
  title={{SpeechBrain}: A General-Purpose Speech Toolkit},
  author={Mirco Ravanelli and Titouan Parcollet and Peter Plantinga and Aku Rouhe and Samuele Cornell and Loren Lugosch and Cem Subakan and Nauman Dawalatabad and Abdelwahab Heba and Jianyuan Zhong and Ju-Chieh Chou and Sung-Lin Yeh and Szu-Wei Fu and Chien-Feng Liao and Elena Rastorgueva and François Grondin and William Aris and Hwidong Na and Yan Gao and Renato De Mori and Yoshua Bengio},
  year={2021},
  eprint={2106.04624},
  archivePrefix={arXiv},
  primaryClass={eess.AS},
  note={arXiv:2106.04624}
}
```
