import argparse
import json

import torch
from pyannote.audio import Pipeline

def main(model: str, audio_path: str, output_path: str, huggingface_auth_token: str | None):
    pipeline = Pipeline.from_pretrained(
        model,
        use_auth_token=huggingface_auth_token)

    # send pipeline to GPU (when available)
    pipeline.to(torch.device("cuda"))

    # apply pretrained pipeline
    diarization = pipeline(audio_path)

    result = []
    # print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        result.append({
            "speaker": speaker,
            "start": turn.start,
            "stop": turn.stop,
        })

    with open(output_path, "w") as out_file:
        diarization.write_rttm(out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="diarize",
    )
    parser.add_argument("audio_path")
    parser.add_argument("-m", "--model", default="pyannote/speaker-diarization-3.1")
    parser.add_argument("-o", "--output", default="/output/diaritization-output.rttm")
    parser.add_argument("-t", "--huggingface-auth-token")

    args = parser.parse_args()

    main(args.audio_path, args.output, args.huggingface_auth_token)