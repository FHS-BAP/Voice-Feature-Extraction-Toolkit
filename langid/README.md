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

`dataset_config_name` and `dataset_split` are specific to each dataset.
Look at a dataset's card on HuggingFace for supported values.

A quick example:
```bash
docker run -it -v output:/output <this container's image> both sanchit-gandhi/whisper-medium-fleurs-lang-id PolyAI/minds14 all 'train[:5]'
```

This evaluates the model `sanchit-gandhi/whisper-medium-fleurs-lang-id` on the dataset `PolyAI/minds14` on first five samples of the `train` split of the `all` config of the dataset (which, for this dataset, includes all languages).

View prediction output and/or generated report will be in the volume mounted to `/output`.
Output includes
- JSON of the predictions and labels
- graphs of model performance
- confusion matrix

The Excel report contains similar information but in human-readable form.

# Supported models and datasets
## Models
- facebook/mms-lid-4017
- sanchit-gandhi/whisper-medium-fleurs

## Datasets
- PolyAI/minds14

## More information
See the model or dataset's card on HuggingFace for more information about each model or dataset.

# Technical Details
You can skip this section unless you are trying to add a new model/dataset or otherwise contribute to the code
## Global IDs
The mapping scripts use "global ids" for each language since `datasets` work better with numerical ids
rather than text ids.
Global ids are based on iso639 part 3 language codes.
The codes are created by treating the code as a 3-digit base-26 number, with a = 0 and z = 25.
So a language code of `yue` has a global id 25 * 26^2 + 20 * 26 + 4