import soundfile
from espnet2.bin.asr_inference import Speech2Text

# model options:
# "Shinji Watanabe/librispeech_asr_train_asr_transformer_e18_raw_bpe_sp_valid.acc.best"
# "kamo-naoyuki/wsj_transformer2",


speech2text = Speech2Text.from_pretrained(
    "Shinji Watanabe/librispeech_asr_train_asr_transformer_e18_raw_bpe_sp_valid.acc.best", #This can be selected from above, or the list given in readme
    # Parameters
    maxlenratio=0.0,
    minlenratio=0.0,
    beam_size=20,
    ctc_weight=0.3,
    lm_weight=0.5,
    penalty=0.0,
    nbest=1
)
# Confirm the sampling rate is equal to that of the training corpus.
# If not, you need to resample the audio data before inputting to speech2text
wav_audio_file = "Example Data/test.wav"

speech, rate = soundfile.read(wav_audio_file)
nbests = speech2text(speech)

text, *_ = nbests[0]

with open('output.txt', 'w') as file:
    #Write transcription to txt file
    file.write(text)

#View output in output.txt