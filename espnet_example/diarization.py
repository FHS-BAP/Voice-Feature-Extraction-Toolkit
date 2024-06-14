"""
File for automatic speaker recognition tasks using espnet.
"""
from scipy.io import wavfile
import io
import soundfile
from IPython.display import display, Audio
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.enh_inference import SeparateSpeech
import matplotlib.pyplot as plt
import torch
from torch_complex.tensor import ComplexTensor
from espnet.asr.asr_utils import plot_spectrogram
from espnet2.layers.stft import Stft


d = ModelDownloader()
tag = "lichenda/Chenda_Li_wsj0_2mix_enh_dprnn_tasnet" #

#Tag options:
# "lichenda/wsj0_2mix_skim_noncausal"
# "espnet/chenda-li-wsj0_2mix_enh_train_enh_conv_tasnet_raw_valid.si_snr.ave"
# "espnet/chenda-li-wsj0_2mix_enh_train_enh_rnn_tf_raw_valid.si_snr.ave"
# "lichenda/Chenda_Li_wsj0_2mix_enh_dprnn_tasnet" #Excellent
# "lichenda/wsj0_2mix_skim_noncausal"
# "espnet/Wangyou_Zhang_wsj0_2mix_enh_dc_crn_mapping_snr_raw"

separate_speech = SeparateSpeech(
  **d.download_and_unpack(tag),
  segment_size=2.4,
  hop_size=0.8,
  normalize_segment_scale=False,
  show_progressbar=True,
  ref_channel=None,
  normalize_output_wav=True,
)

speech, rate_ = soundfile.read("Example Data/Sample_InClinic_Clip_Mono_Short.wav") #Example audio file included, can be changed

waves = separate_speech(speech[None, ...], fs=rate_)


spk1 = waves[0].squeeze()
spk2 = waves[1].squeeze()

wav1_io = io.BytesIO()
wav2_io = io.BytesIO()
wavfile.write(wav1_io, rate_, spk1)
wavfile.write(wav2_io, rate_, spk2)

# Writing separated speech to 2 separate wav files, one for speaker 1 and one for speaker 2

with open('spk1.wav', 'wb') as f:
    f.write(wav1_io.getvalue())

with open('spk2.wav', 'wb') as f:
    f.write(wav2_io.getvalue())



display(Audio(speech, rate=rate_))


#Code below is for visual output giving spectrograms of separate speakers


stft = Stft(
  n_fft=512,
  win_length=None,
  hop_length=128,
  window="hann",
)

ilens = torch.LongTensor([len(speech)])

stft = Stft(
  n_fft=512,
  win_length=None,
  hop_length=128,
  window="hann",
)
ilens = torch.LongTensor([len(speech)])
# specs: (T, F)
spec_mix = ComplexTensor(
    *torch.unbind(
      stft(torch.as_tensor(speech).unsqueeze(0), ilens)[0].squeeze(),
      dim=-1
  )
)
spec_sep1 = ComplexTensor(
    *torch.unbind(
      stft(torch.as_tensor(waves[0]), ilens)[0].squeeze(),
      dim=-1
  )
)
spec_sep2 = ComplexTensor(
    *torch.unbind(
      stft(torch.as_tensor(waves[1]), ilens)[0].squeeze(),
      dim=-1
  )
)

# freqs = torch.linspace(0, rate_ / 2, spec_mix.shape[1])
# frames = torch.linspace(0, len(speech) / rate_, spec_mix.shape[0])
samples = torch.linspace(0, len(speech) / rate_, len(speech))
plt.figure(figsize=(24, 12))
plt.subplot(3, 2, 1)
plt.title('Mixture Spectrogram')
plot_spectrogram(
  plt, abs(spec_mix).transpose(-1, -2).numpy(), fs=rate_,
  mode='db', frame_shift=None,
  bottom=False, labelbottom=False
)
plt.subplot(3, 2, 2)
plt.title('Mixture Wavform')
plt.plot(samples, speech)
plt.xlim(0, len(speech) / rate_)

plt.subplot(3, 2, 3)
plt.title('Separated Spectrogram (spk1)')
plot_spectrogram(
  plt, abs(spec_sep1).transpose(-1, -2).numpy(), fs=rate_,
  mode='db', frame_shift=None,
  bottom=False, labelbottom=False
)
plt.subplot(3, 2, 4)
plt.title('Separated Wavform (spk1)')
plt.plot(samples, waves[0].squeeze())
plt.xlim(0, len(speech) / rate_)

plt.subplot(3, 2, 5)
plt.title('Separated Spectrogram (spk2)')
plot_spectrogram(
  plt, abs(spec_sep2).transpose(-1, -2).numpy(), fs=rate_,
  mode='db', frame_shift=None,
  bottom=False, labelbottom=False
)
plt.subplot(3, 2, 6)
plt.title('Separated Wavform (spk2)')
plt.plot(samples, waves[1].squeeze())
plt.xlim(0, len(speech) / rate_)
plt.xlabel("Time (s)")
plt.show()
plt.savefig('plot.png')