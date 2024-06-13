# Spacy

## API Endpoints

### `/tokenize`

- **Method**: POST
- **Description**: Tokenizes the input text into words or punctuation marks.
- **Payload**: `{"text": "Your input text here."}`
- **Response**: `{"tokens": ["Your", "input", "text", "here", "."]}`

### `/pos_tag`

- **Method**: POST
- **Description**: Provides part-of-speech tags for each token in the input text.
- **Payload**: `{"text": "Your input text here."}`
- **Response**: `{"pos_tags": [["Your", "PRON"], ["input", "NOUN"], ...]}`

### `/dep_parse`

- **Method**: POST
- **Description**: Returns the dependency parse of the input text.
- **Payload**: `{"text": "Your input text here."}`
- **Response**: `{"dep_parse": [["Your", "poss"], ["input", "compound"], ...]}`

### `/lemmatize`

- **Method**: POST
- **Description**: Reduces words in the input text to their lemma forms.
- **Payload**: `{"text": "Your input text here."}`
- **Response**: `{"lemmas": ["your", "input", "text", "here", "."]}`

### `/sbd`

- **Method**: POST
- **Description**: Identifies sentence boundaries in the input text.
- **Payload**: `{"text": "Your input text here. Another sentence here."}`
- **Response**: `{"sentences": ["Your input text here.", "Another sentence here."]}`

### `/ner`

- **Method**: POST
- **Description**: Recognizes named entities in the input text.
- **Payload**: `{"text": "John Doe lives in New York."}`
- **Response**: `{"entities": [["John Doe", "PERSON"], ["New York", "GPE"]]}`

## How to use

cd into this directory and run the following command:

```bash
./test.sh
```

It will setup the docker container, and iterate through the subroutines to demonstrate the functionalities.

## Updating subroutines

For customizing the inputs, you would need to upload your files of interest, and updates the subroutines to target them.

## Citation

None found. MIT License included instead.
