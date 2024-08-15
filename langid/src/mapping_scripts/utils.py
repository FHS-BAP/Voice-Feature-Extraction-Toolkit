import json
from pathlib import Path

def save_mappings(output_folder_path: Path, model_id_to_global_id, global_id_to_model_id):
  output_folder_path.mkdir(parents=True, exist_ok=True)
  
  with open(output_folder_path / "model_id_to_global_id.json", "w") as out_file:
      json.dump(model_id_to_global_id, out_file)

  with open(output_folder_path / "global_id_to_model_id.json", "w") as out_file:
    json.dump(global_id_to_model_id, out_file)