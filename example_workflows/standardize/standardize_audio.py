"""
standardize_audio.py
standardize audio extension, encoding, and sampling rate
"""
import os
import ffmpeg
from misc import read_json, write_json, get_dt_now, get_audio_files

def write_metadata(root, audio_exts):
    """
    get metadata via ffmpeg and then write to a JSON file
    """
    final = []
    audio_filepaths = get_audio_files(root, audio_exts)
    for audio_fp in audio_filepaths:
        metadata = ffmpeg.probe(audio_fp)
        final.append({'audio_fp': audio_fp, 'metadata': metadata})
    root_ext = os.path.basename(os.path.normpath(root))
    json_out = f'output/write_metadata_to_json/{get_dt_now()}/{root_ext}_audio_metadata.json'
    write_json(final, json_out)
    return json_out

def downsample(wav_fp, out_fp, **kwargs):
    """
    downsample a WAV file to 16KHz sampling rate and a bit depth of 16 (PCM_s16le)
    """
    if not os.path.isdir(os.path.dirname(out_fp)):
        os.makedirs(os.path.dirname(out_fp))
    stream = ffmpeg.input(wav_fp)
    stream = ffmpeg.output(stream, out_fp, **kwargs)
    stream.run(overwrite_output=True)

def downsample_audio_files(json_in, audio_in_root, std_audio_ext, **kwargs):
    """
    read in a JSON and attempt to downsample each audio_fp
    """
    if json_in is not None:
        all_audio_fps = [d['audio_fp'] for d in read_json(json_in)]
    else:
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
    config_list = [read_json('config/config.json'),
        read_json('config/check_downsample_config.json')]
    for config in config_list:
        audio_in_root = config['audio_in_root']
        audio_in_exts = config['audio_in_exts']
        audio_in_exts = audio_in_exts if audio_in_exts is None else\
            tuple((e.lower() for e in audio_in_exts))
        ## leave audio_in_exts as None if it's None,
        ## otherwise convert to tuple and lowercase each ext
        if config['do_write_metadata']:
            print(f'writing metadata: ({audio_in_root}, {audio_in_exts})')
            json_out = write_metadata(audio_in_root, audio_in_exts)
        else:
            json_out = None
            print('skipping metadata writing')
        if config['do_downsample']:
            std_kw = {'c:a': config['std_audio_encoding'], 'ar': config['std_sampling_rate'],
                'loglevel': config['std_log_level']}
            json_in = config.get('std_json_in', json_out)
            downsample_audio_files(json_in, audio_in_root, config['std_audio_ext'],
                **std_kw)
        else:
            print('skipping downsampling')
        print()

if __name__ == '__main__':
    main()
