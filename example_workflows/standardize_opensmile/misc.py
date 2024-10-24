"""
misc.py
miscellaneous functions for reading/writing files and iterating input files
"""
import os
import json

def read_json(json_in):
    """
    read a json file
    """
    with open(json_in, 'r') as infile:
        final = json.load(infile)
    return final

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
