# Language Identification
Container to run and evaluate different language identification models on different datasets.

# Usage
This container writes the evaluation output in the `/output` directory within the container
```bash
docker run <this container's image> (evaluate|report|both) <model_id> <dataset_id> <dataset_config_name> <dataset_split>
```

`evaluate` runs the model and evaluates its predictions.
`report` creates an Excel report of the model's performance.
Requires that an `evaluate` command was run previously to create model's predictions.
`both` runs both `evaluate` and `report`.

See [below](#supported-models-and-datasets) for supported values for `model_id` and `dataset_id`

`dataset_config_name` and `dataset_split` are dataset-specific names for different subsets of a dataset.
See the dataset card on HuggingFace for the config name and splits defined in a particular dataset.
Generally, for spoken language datasets, the config name is a language subset
and the split is one of train, dev, test, and val.

Output includes
- JSON of the predictions and labels
- graphs of model performance
- confusion matrix
The Excel report contains similar information but in human-readable form.

## Example
```bash
docker run -it -v output:/output <this container's image> both sanchit-gandhi/whisper-medium-fleurs-lang-id PolyAI/minds14 all 'train[:5]'
```

This evaluates the model `sanchit-gandhi/whisper-medium-fleurs-lang-id` on the dataset `PolyAI/minds14` on first five samples of the `train` split of the `all` config of the dataset (which, for this dataset, includes all languages).

# Output
View prediction output and/or generated report will be in the volume mounted to `/output`.

# Supported models and datasets
## Models
- [facebook/mms-lid-4017](https://huggingface.co/facebook/mms-lid-4017)
- [sanchit-gandhi/whisper-medium-fleurs](https://huggingface.co/sanchit-gandhi/whisper-medium-fleurs-lang-id)

## Datasets
- [PolyAI/minds14](https://huggingface.co/datasets/PolyAI/minds14)

## More information
See the model or dataset's card on HuggingFace for more information about each model or dataset.

# Performance
The following table lists performance of select model and dataset combinations on small subsets of the datasets (due to performance limitations).
For more information, a model's card on HuggingFace may have their own benchmark results.

| Model \ Dataset                                   | PolyAI/minds14                                    |
| ------------------------------------------------  | ------------------------------------------------  |
| **sanchit-gandhi/whisper-medium-fleurs-lang-id**  | Accuracy: 62%, F1 Macro: 0.19, F1 Micro: 0.62     |
| **facebook/mms-lid-4017**                         | Accuracy: 88%, F1 Macro: 0.23, F1 Micro: 0.88     |

# Technical Details
You can skip this section unless you are trying to add a new model/dataset or otherwise contribute to the code
## Global IDs
The mapping scripts use "global ids" for each language since `datasets` work better with numerical ids
rather than text ids.
Global ids are based on iso639 part 3 language codes.
The codes are created by treating the code as a 3-digit base-26 number, with a = 0 and z = 25.
So a language code of `yue` has a global id 25 * 26^2 + 20 * 26 + 4

## Standard dataset format
A standard format for datasets is used as a common interface between the dataset and model preprocessing scripts.
A dataset's preprocessing script should create a dataset in the standard format
and a model should process the standard format dataset into a model-specific format.

The standard format has two columns:
- `lang_id`: the language global id of the sample. An `int32` column, using the `datasets` types
- `audio`: the audio of the sample. Make sure this `datasets` `Audio`