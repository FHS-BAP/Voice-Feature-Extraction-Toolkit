from typing import Any

import datasets

def load(name: str, split: str, other_args: dict[str, Any] | None=None):
    dataset = (datasets
        .load_dataset("amaai-lab/DisfluencySpeech", name=name, split=split, **(other_args or {}), trust_remote_code=True)
        .cast_column("audio", datasets.Audio(sampling_rate=16_000))
        # transcript_a seems to include disfluency
        .select_columns(("audio", "transcript_a"))
        .rename_column("transcript_a", "transcription"))

    return dataset