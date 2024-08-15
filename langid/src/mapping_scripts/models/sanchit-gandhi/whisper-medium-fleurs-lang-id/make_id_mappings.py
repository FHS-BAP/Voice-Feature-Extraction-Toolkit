from pathlib import Path
import json

from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

model_id = "sanchit-gandhi/whisper-medium-fleurs-lang-id"

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
  # This model was trained in google/fleurs, so we can reuse the mappings from the dataset
  # Copied from https://huggingface.co/datasets/google/fleurs/blob/main/fleurs.py
  from collections import OrderedDict
  FLEURS_LANG_TO_ID = OrderedDict([("Afrikaans", "af"), ("Amharic", "am"), ("Arabic", "ar"), ("Armenian", "hy"), ("Assamese", "as"), ("Asturian", "ast"), ("Azerbaijani", "az"), ("Belarusian", "be"), ("Bengali", "bn"), ("Bosnian", "bs"), ("Bulgarian", "bg"), ("Burmese", "my"), ("Catalan", "ca"), ("Cebuano", "ceb"), ("Mandarin Chinese", "cmn_hans"), ("Cantonese Chinese", "yue_hant"), ("Croatian", "hr"), ("Czech", "cs"), ("Danish", "da"), ("Dutch", "nl"), ("English", "en"), ("Estonian", "et"), ("Filipino", "fil"), ("Finnish", "fi"), ("French", "fr"), ("Fula", "ff"), ("Galician", "gl"), ("Ganda", "lg"), ("Georgian", "ka"), ("German", "de"), ("Greek", "el"), ("Gujarati", "gu"), ("Hausa", "ha"), ("Hebrew", "he"), ("Hindi", "hi"), ("Hungarian", "hu"), ("Icelandic", "is"), ("Igbo", "ig"), ("Indonesian", "id"), ("Irish", "ga"), ("Italian", "it"), ("Japanese", "ja"), ("Javanese", "jv"), ("Kabuverdianu", "kea"), ("Kamba", "kam"), ("Kannada", "kn"), ("Kazakh", "kk"), ("Khmer", "km"), ("Korean", "ko"), ("Kyrgyz", "ky"), ("Lao", "lo"), ("Latvian", "lv"), ("Lingala", "ln"), ("Lithuanian", "lt"), ("Luo", "luo"), ("Luxembourgish", "lb"), ("Macedonian", "mk"), ("Malay", "ms"), ("Malayalam", "ml"), ("Maltese", "mt"), ("Maori", "mi"), ("Marathi", "mr"), ("Mongolian", "mn"), ("Nepali", "ne"), ("Northern-Sotho", "nso"), ("Norwegian", "nb"), ("Nyanja", "ny"), ("Occitan", "oc"), ("Oriya", "or"), ("Oromo", "om"), ("Pashto", "ps"), ("Persian", "fa"), ("Polish", "pl"), ("Portuguese", "pt"), ("Punjabi", "pa"), ("Romanian", "ro"), ("Russian", "ru"), ("Serbian", "sr"), ("Shona", "sn"), ("Sindhi", "sd"), ("Slovak", "sk"), ("Slovenian", "sl"), ("Somali", "so"), ("Sorani-Kurdish", "ckb"), ("Spanish", "es"), ("Swahili", "sw"), ("Swedish", "sv"), ("Tajik", "tg"), ("Tamil", "ta"), ("Telugu", "te"), ("Thai", "th"), ("Turkish", "tr"), ("Ukrainian", "uk"), ("Umbundu", "umb"), ("Urdu", "ur"), ("Uzbek", "uz"), ("Vietnamese", "vi"), ("Welsh", "cy"), ("Wolof", "wo"), ("Xhosa", "xh"), ("Yoruba", "yo"), ("Zulu", "zu")])
  FLEURS_LANG_SHORT_TO_LONG = {v: k for k, v in FLEURS_LANG_TO_ID.items()}

  model_id_to_global_id = {
    model_id: global_id_utils.language_to_global_id(FLEURS_LANG_TO_ID[model.config.id2label[model_id]].split("_")[0])
    for model_id in model.config.id2label
  }
  ##############

  global_id_to_model_id = {v:k for k, v in model_id_to_global_id.items()}

  return model_id_to_global_id, global_id_to_model_id

if __name__ == "__main__":
  output_folder_path = Path(__file__).resolve().parents[4] / "mappings" / "models" / model_id
  model_ids_to_global_ids, global_ids_to_model_ids = create_mappings()
  utils.save_mappings(output_folder_path, model_ids_to_global_ids, global_ids_to_model_ids)