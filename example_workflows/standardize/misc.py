"""
misc.py
miscellaneous functions for reading/writing files and iterating input files
"""
import os
import json
from datetime import datetime

def read_json(json_in):
    """
    read a json file
    """
    with open(json_in, 'r') as infile:
        final = json.load(infile)
    return final

def write_json(final, json_out):
    """
    write JSON file
    make necessary subdirs
    """
    parent = os.path.dirname(json_out)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with open(json_out, 'w') as outfile:
        json.dump(final, outfile, sort_keys=True, indent=4)
    print(f'wrote {json_out}')

def get_dt_now():
	"""
	convert datetime.now() output to a str that can be used for naming directories
	"""
	return str(datetime.now()).replace(" ", "_").replace(":", "_").split(".")[0]

def get_audio_files(root, audio_exts):
    """
    getting audio files with an ext in audio_exts
    """
    audio_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if audio_exts is None or full_path.lower().endswith(audio_exts):
                audio_files.append(full_path)
    return audio_files
