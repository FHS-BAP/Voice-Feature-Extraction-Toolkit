import datasets

def to_standard_dataset(dataset, dataset_id_to_global_id):
  """Performs preprocessing to transform dataset into a standard format so that model preprocessing scripts can work"""
  def preprocess(sample):
    sample["lang_id"] = dataset_id_to_global_id[sample["lang_id"]]
    return sample

  new_features = dataset.features.copy()
  new_features["lang_id"] = datasets.Value("int32")
  
  dataset = (dataset
              .cast(new_features)
              .select_columns(["lang_id", "audio"])
              .map(preprocess, batched=False))
  return dataset