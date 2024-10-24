"""
osm.py
opensmile functions
"""
import os
import opensmile
import soundfile as sf

def extract_osm_features(audio_fn, csv_out, feat_level='lld'):
    """
    Extracts frequency characteristics of audio using OpenSMILE.

    Writes the features to a CSV

    """
    assert feat_level in {'lld', 'functionals'}, feat_level
    if feat_level == 'lld':
        feature_level = opensmile.FeatureLevel.LowLevelDescriptors
    elif feat_level == 'functionals':
        feature_level = opensmile.FeatureLevel.Functionals

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.ComParE_2016,
        feature_level=feature_level,
    )

    audio_samples, audio_sample_rate = sf.read(audio_fn)
    if len(audio_samples.shape) == 2:
        audio_samples = audio_samples[:, 0]
    features = smile.process_signal(audio_samples, audio_sample_rate)
    parent = os.path.dirname(csv_out)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    features.to_csv(csv_out)
    print(csv_out)
