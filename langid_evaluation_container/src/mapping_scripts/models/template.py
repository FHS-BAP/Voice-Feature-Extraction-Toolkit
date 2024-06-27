from pathlib import Path
import json

from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

model_id = "MODEL_NAME_HERE"

if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import global_id_utils
import utils

def create_mappings():
  """
  Returns the model id to global id dictionary and global id to model id dictionary as a tuple
  """
  model = AutoModelForAudioClassification.from_pretrained(model_id)
  # model.to_bettertransformer()
  feature_extractor = AutoFeatureExtractor.from_pretrained(model_id)

  modified_id2label = model.config.id2label.copy()
  ##############
  # Custom code here
  ##############

  model_id_to_global_id = {
      model_id: global_id_utils.language_to_global_id(modified_id2label[model_id].split("_")[0])
      for model_id in model.config.id2label
  }

  global_id_to_model_id = {v:k for k, v in model_id_to_global_id.items()}

  return model_id_to_global_id, global_id_to_model_id

if __name__ == "__main__":
  output_folder_path = Path(f"mappings/models/{model_id}")
  model_ids_to_global_ids, global_ids_to_model_ids = create_mappings()
  utils.save_mappings(output_folder_path, model_ids_to_global_ids, global_ids_to_model_ids)