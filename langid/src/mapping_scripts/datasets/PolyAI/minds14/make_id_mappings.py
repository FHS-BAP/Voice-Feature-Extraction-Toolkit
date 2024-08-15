from pathlib import Path
import json

import iso639
import datasets

if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append("/app")
import global_id_utils

def create_mappings(output_folder_path: Path):
  """
  Returns the model id to global id dictionary and global id to model id dictionary as a tuple
  """
  dataset_id = "PolyAI/minds14"
  lang_id_column_name = "lang_id"
  dataset = datasets.load_dataset("PolyAI/minds14", "all", split="train", trust_remote_code=True)

  int2str = dataset.features[lang_id_column_name]._int2str
  str2int = dataset.features[lang_id_column_name]._str2int

  dataset_id_to_global_id = {
    dataset_id: global_id_utils.iso639_part3_to_global_id(
        iso639.Language.from_part1(int2str[dataset_id].split("-")[0]).part3)
    for dataset_id in str2int.values()
  }
  dataset_id_to_global_id[str2int["zh-CN"]] = global_id_utils.iso639_part3_to_global_id("cmn")

  with open(output_folder_path / "dataset_id_to_global_id.json", "w") as out_file:
    json.dump(dataset_id_to_global_id, out_file)

  with open(output_folder_path / "global_id_to_dataset_id.json", "w") as out_file:
    json.dump(dataset_id_to_global_id, out_file)

if __name__ == "__main__":
  output_folder_path = Path("mappings/datasets/PolyAI/minds14")
  output_folder_path.mkdir(parents=True, exist_ok=True)
  create_mappings(output_folder_path)