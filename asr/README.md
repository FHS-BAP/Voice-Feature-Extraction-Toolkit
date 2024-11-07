# ASR
Container to run and evaluate different automatic speech recognition (ASR) models on different datasets.

Includes models and datasets for verbatim transcription, which include disfluencies such as "uh" and "um".

# Usage
```bash
docker run -it <image_id> -v <container-output>:/output (predict|evaluate) <model_id> <dataset_id> <dataset_config_name> <dataset_split>
```

The container writes output to the `/output` folder. Mount a folder on the host to save and view the output with the `-v` or `--mount` flags.

`model_id` and `dataset_id` are the ids of the ASR model and dataset, respectively, to evaluate.
See [Available Models](#available-models) and [Available Datasets](#available-datasets) for a list of currently implemented models and datasets. See HuggingFace for more information about each model and dataset.

`dataset_config_name` and `dataset_split` are dataset-specific names for different subsets of a dataset.
See the dataset card on HuggingFace for the config name and splits defined in a particular dataset.
Generally, for spoken language datasets, the config name is a language subset
and the split is one of train, dev, test, and val.

## Example
```bash
docker run -it <image_id> -v container-output:/output NbAiLabBeta/nb-whisper-medium-verbatim amaai-lab/DisfluencySpeech default train[:5]
```

This evaluates the model `NbAiLabBeta/nb-whisper-medium-verbatim` on the first five samples in the train split of the default subset  of the dataset `amaai-lab/DisfluencySpeech`.

## Output
The container's output will be JSON files in the output volume.
JSON files include:
- Model transcriptions and ground truth transcriptions

# Available Models
## General ASR
- [openai/whisper-base](https://huggingface.co/openai/whisper-base)
## Verbatim
- [openai/whisper-base/prompting](https://huggingface.co/openai/whisper-base) (openai/whisper-base with prompting)
- [NbAiLabBeta/nb-whisper-medium-verbatim](https://huggingface.co/NbAiLabBeta/nb-whisper-medium-verbatim)

# Available Datasets
## General ASR
- [PolyAI/minds14](https://huggingface.co/datasets/PolyAI/minds14)
## Verbatim
- [amaai-lab/DisfluencySpeech](https://huggingface.co/datasets/amaai-lab/DisfluencySpeech)
