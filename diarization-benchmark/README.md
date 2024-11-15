Docker container based on https://github.com/Picovoice/speaker-diarization-benchmark

Benchmarks several diarization engines/models, reporting several metrics including
Diarization Error Rate, Jaccard Error Rate, and CPU and memory usage.

Currently, no new models or datasets have been added. All benchmarks are from upstream.

Uses the [Voxconverse](https://github.com/joonson/voxconverse) dataset

# Usage
To run a benchmark with a chosen engine and dataset,
```bash
python3 benchmark.py \
--type (ACCURACY | CPU | MEMORY) \
--dataset VoxConverse \
--data-folder (/data/voxconverse/wav/dev | /data/voxconverse/wav/test) \
--label-folder /data/voxconverse/labels/ \
--engine <engine> \
<additional arguments depending on engine>
```

Output is printed in the terminal.
The upstream documentation does not cover whether output is written to files.

For the additional arguments required for each engine, see the [upstream documentation](https://github.com/Picovoice/speaker-diarization-benchmark?tab=readme-ov-file#data)

## Example
An example using pyannote is given because Pyannote is free

To use Pyannote, you must first accept the conditions at its [Huggingface page](https://huggingface.co/pyannote/speaker-diarization), then create a Huggingface token.

```bash
python3 benchmark.py \
--dataset VoxConverse \
--data-folder /data/voxconverse/wav/test \
--label-folder /data/voxconverse/labels/ \
--engine PYANNOTE \
--type ACCURACY \
--pyannote-auth-token <HUGGINGFACE_TOKEN>
```

## Further help
See the [upstream repo](https://github.com/pyannote/pyannote-audio) for more details 
including other supported engines and arguments.
