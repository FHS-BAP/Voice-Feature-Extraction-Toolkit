"""
standardize_audio.py
standardize audio extension, encoding, and sampling rate
"""
import os
import ffmpeg
from misc import read_json, get_audio_files
from osm import extract_osm_features

def downsample(wav_fp, out_fp, **kwargs):
    """
    downsample a WAV file to 16KHz sampling rate and a bit depth of 16 (PCM_s16le)
    """
    if not os.path.isdir(os.path.dirname(out_fp)):
        os.makedirs(os.path.dirname(out_fp))
    stream = ffmpeg.input(wav_fp)
    stream = ffmpeg.output(stream, out_fp, **kwargs)
    stream.run(overwrite_output=True)

def downsample_audio_files(audio_in_root, std_audio_ext, **kwargs):
    """
    read in a JSON and attempt to downsample each audio_fp
    """
    all_audio_fps = get_audio_files(audio_in_root, (std_audio_ext.lower(), ))

    for audio_fp in all_audio_fps:
        audio_dir = f'output/downsampled_{std_audio_ext}'
        audio_fn = os.path.splitext(os.path.basename(audio_fp))[0]
        out_fp = os.path.join(audio_dir, f'downsampled_{audio_fn}.{std_audio_ext}')
        print(f'Downsampling to: {out_fp}')
        downsample(audio_fp, out_fp, **kwargs)

def main():
    """
    main entrypoint, see README.md for further documentation
    """
    config = read_json('config/config.json')
    audio_in_root = config['audio_in_root']
    audio_in_exts = config['audio_in_exts']
    audio_in_exts = audio_in_exts if audio_in_exts is None else\
        tuple((e.lower() for e in audio_in_exts))
    ## leave audio_in_exts as None if it's None,
    ## otherwise convert to tuple and lowercase each ext

    std_audio_ext = config.get('std_audio_ext')
    if config['do_downsample']:
        std_kw = {'c:a': config['std_audio_encoding'], 'ar': config['std_sampling_rate'],
            'loglevel': config['std_log_level']}
        downsample_audio_files(audio_in_root, std_audio_ext,
            **std_kw)
        osm_input_root = f'output/downsampled_{std_audio_ext}/'
    else:
        print('skipping downsampling')
        osm_input_root = audio_in_root
    osm_feat_list = config['osm_feat_list']
    for feat in osm_feat_list:
        for audio_fp in get_audio_files(osm_input_root, std_audio_ext):
            audio_fn = os.path.splitext(os.path.basename(audio_fp))[0]
            csv_out = os.path.join(f'output/osm/{audio_fn}_{feat}.csv')
            extract_osm_features(audio_fp, csv_out, feat_level=feat)

if __name__ == '__main__':
    main()
