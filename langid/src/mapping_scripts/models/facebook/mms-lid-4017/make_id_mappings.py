from pathlib import Path
import json

from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

model_id = "facebook/mms-lid-4017"

if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    # global_id_utils
    sys.path.append("/app")
    # mapping script utils
    sys.path.append("/app/mapping_scripts")

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
  id2label = model.config.id2label
  xdn_id = next(id for id, label in id2label.items() if label == "xdn")
  # "xdn" doesn't appear to be a valid language
  del modified_id2label[xdn_id]
  # "plj" is deprecated for Polci (https://iso639-3.sil.org/code_tables/deprecated_codes/data?title=plj&name=&field_iso639_element_scope_tid=All&field_iso639_language_type_tid=All)
  plj_id = next(id for id, label in id2label.items() if label == "plj")
  # "pze" is one dialect of "Polci". Assuming that 
  modified_id2label[plj_id] = "pze"
  # "ksa" deprecated: https://iso639-3.sil.org/code/ksa
  ksa_id = next(id for id, label in id2label.items() if label == "ksa")
  modified_id2label[ksa_id] = "izm"

  model_id_to_global_id = {
    model_id: global_id_utils.language_to_global_id(modified_id2label[model_id].split("_")[0])
    for model_id in modified_id2label
  }

  # "xdn" doesn't appear to be a valid language
  model_id_to_global_id[xdn_id] = -1
  ##############

  global_id_to_model_id = {v:k for k, v in model_id_to_global_id.items()}

  return model_id_to_global_id, global_id_to_model_id

if __name__ == "__main__":
  output_folder_path = Path(f"mappings/models/{model_id}")
  model_ids_to_global_ids, global_ids_to_model_ids = create_mappings()
  utils.save_mappings(output_folder_path, model_ids_to_global_ids, global_ids_to_model_ids)