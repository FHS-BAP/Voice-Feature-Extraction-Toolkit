import iso639

def lower_letter_to_num(letter:str) -> int:
  """Returns the index of the english lowercase letter in the alphabet, with a zero-based index.
  The input string must be a single character and a lowercase letter.
  >>> lower_letter_to_num("a")
  0
  >>> lower_letter_to_num("z")
  25
  >>> lower_letter_to_num("k")
  10
  """
  assert len(letter) == 1, f'Letter "{letter}" must be a single letter'
  letter_ascii = ord(letter)
  letter_num = letter_ascii - ord('a')
  assert 0 <= letter_num <= 26, f'Letter "{letter}" must be a lowercase English (ASCII) letter'
  return letter_num
  
def iso639_part3_to_global_id(lang:str) -> int:
  """Converts an ISO 639-3 language to a unique integer id used across all models and datasets.
  ISO 639-3 is already a unique identifier, but parts of Huggingface modules require integers.

  Interprets the letters in the ISO 639-3 code as a base-26 number and converts that to an integer

  >>> iso639_part3_to_global_id("yue")
  16748
  >>> iso639_part3_to_global_id("eng")
  3048
  """
  assert len(lang) == 3, f'lang must be an ISO 639-3 language code. Got "{lang}"'
  return 26**2 * lower_letter_to_num(lang[0]) + 26 * lower_letter_to_num(lang[1]) + lower_letter_to_num(lang[2])
  
def letter_num_to_letter(letter_num:int) -> str:
  assert 0 <= letter_num < 26
  return chr(ord('a') + letter_num)
  
def global_id_to_iso639_part3(id:int) -> str:
  return letter_num_to_letter((id // (26 * 26)) % 26) + letter_num_to_letter((id // 26) % 26) + letter_num_to_letter(id % 26)
  
def language_to_global_id(lang:str) -> int:
  return iso639_part3_to_global_id(iso639.Language.match(lang).part3)

def global_id_to_lang(id:int) -> iso639.Language:
  lang_part3 = global_id_to_iso639_part3(id)
  lang = iso639.Language.from_part3(lang_part3)
  return lang