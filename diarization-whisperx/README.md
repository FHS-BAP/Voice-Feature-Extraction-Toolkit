Docker container for transcription using [WhisperX](https://github.com/mbain/whisperX)
combined with diarization using Pyannote.

# Usage
The basic usage is
```bash
docker run -it -b <audio volume or path>:/data <image id> [--diarize] [--compute_type (float16 | float32 |int8)] [--hf_token <huggingface token>] <audio path inside container> [<audio path inside container>...]
```

WhisperX runs in `/data`, so paths should be relative to `/data`.

This command will transcribe and align the given audio file, writing output to in several formats including
- json
- txt
- srt
- tsv
- vtt

Output will be created in the working directory (`/data` by default).

Output files are named after the original audio file.

By default, WhisperX will run only transcription with word timings. To also enable diarization, add the `--diarize` flag.
Diarization uses Pyannote/speaker-diarization-3.1, so you must accept Pyannote's conditions first.
1. Go to [Pyannote's Huggingface page](https://huggingface.co/pyannote/speaker-diarization-3.1)
2. Accept their terms and conditions
3. Create a Huggingface access token
4. Pass the access token with the `--hf_token` flag

When running with CPU, `--compute_type float32` may be required.

## Example
```bash
docker run -it -b ./audio/:/data <image id> --diarize --compute_type float32 --hf_token <huggingface token> example.wav
```

This assumes an example audio file `./audio/example.wav`. Output will be placed in `./audio/`.

## Further details
For a full list of command line flags, run with the `--help` flag.

For more details, see the [WhisperX repo](https://github.com/m-bain/whisperX)