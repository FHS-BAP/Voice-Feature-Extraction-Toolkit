from typing import Any

import datasets

def load(name: str, split: str, other_args: dict[str, Any] | None=None):
    dataset = (datasets
        .load_dataset("hf-internal-testing/librispeech_asr_dummy", name=name, split=split, **(other_args or {}), trust_remote_code=True)
        .cast_column("audio", datasets.Audio(sampling_rate=16_000))
        .select_columns(("audio", "text"))
        .rename_column("text", "transcription"))

    return dataset