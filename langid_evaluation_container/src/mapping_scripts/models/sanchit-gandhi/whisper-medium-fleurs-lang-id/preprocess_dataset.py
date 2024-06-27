import torch
import datasets

def to_model_dataset(dataset, model, feature_extractor, global_id_to_model_id):
  """Performs preprocessing to transform a standard dataset into a dataset that can be processed by the model"""
  # assert len(feature_extractor.model_input_names) == 1, "More than 1 model input name. Manually specific column name"
  # model_input_column_name = next(name for name in feature_extractor.model_input_names if name != "attention_mask")

  def preprocess(sample):
    new_sample = feature_extractor(sample["audio"]["array"], sampling_rate=sample["audio"]["sampling_rate"], return_tensors="pt")
    for input_feature in feature_extractor.model_input_names:
      new_sample[input_feature] = torch.squeeze(new_sample[input_feature])
    global_id = sample["lang_id"]
    new_sample["label"] = global_id_to_model_id[global_id]
    return new_sample

  return (dataset
          .cast_column("audio", datasets.Audio(sampling_rate=16000))
          .map(preprocess, batched=False, remove_columns=["audio"]))