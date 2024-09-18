from flask import Flask, request, jsonify
import re
import sys
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy
from taaled import ld
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import sentiwordnet as swn
from transformers import T5Tokenizer, T5ForConditionalGeneration
from collections import Counter, defaultdict
import whisperx
import gc
import torch
import numpy as np
import spacy
from spacy import displacy
import itertools
import gc
from pydub import AudioSegment
import os
import logging
import librosa

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create the Flask app
app = Flask(__name__)

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Download the NLTK punkt tokenizer
nltk.download('punkt', quiet=True)
nltk.download('sentiwordnet', quiet=True)
nltk.download('wordnet', quiet=True)

# Load the tokenizer and model
model_name = "mixedbread-ai/mxbai-embed-large-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load T5 model and tokenizer
action_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
action_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

def is_negative_adverb(word: str) -> bool:
    input_text = f'Please answer the following question with yes or no. Negative adverbs include the word "not" and "neither". Is "{word}" a negative adverb?'
    input_ids = action_tokenizer(input_text, return_tensors="pt").input_ids

    outputs = action_model.generate(input_ids)
    output_str = action_tokenizer.decode(outputs[0], skip_special_tokens=True).lower()
    if output_str == "yes":
        return True
    elif output_str == "no":
        return False
    raise ValueError(f"Model returned '{output_str}'. Cannot parse to yes or no.")

def is_negative_sentiment(word: str, neg_score_threshold=0.1):
    try:
        first_sentisynset = next(swn.senti_synsets(word))
        return first_sentisynset.neg_score() > neg_score_threshold
    except StopIteration:
        return False

def negative_adverb_rate(text: str):
    doc = nlp(text)
    total_token_count = 0
    negative_adverb_count = 0
    for token in doc:
        if token.pos_ == "PUNCT":
            continue
        total_token_count += 1
        if token.pos_ in ("ADV", "CCONJ"):
            if is_negative_adverb(token.text):
                negative_adverb_count += 1

    return negative_adverb_count / total_token_count if total_token_count > 0 else 0

def is_action_verb(word: str) -> bool:
    input_text = f'Please answer the following question. An action verb is a verb referring to physical action like to put, to run, or to eat. Is "{word}" an action verb?'
    input_ids = action_tokenizer(input_text, return_tensors="pt").input_ids

    outputs = action_model.generate(input_ids)
    output_str = action_tokenizer.decode(outputs[0], skip_special_tokens=True).lower()
    if output_str == "yes":
        return True
    elif output_str == "no":
        return False
    raise ValueError(f"Model returned '{output_str}'. Cannot parse to yes or no.")

def action_verb_rate(text: str):
    doc = nlp(text)

    total_token_count = len(doc)
    action_verb_count = sum(1 for token in doc if token.pos_ == "VERB" and is_action_verb(token.text))
    return action_verb_count / total_token_count

def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.cpu().numpy()

# Helper functions
def pausing_behavior(audio, device: str = "cpu"):
    """
    audio is a column of a dataset with audio at 16 000 Hz sampling rate
    """
    logging.info("Starting pausing_behavior function")
    compute_type = "float32"
    batch_size = 16

    # 1. Transcribe with original whisper (batched)
    logging.info("Loading Whisper model")
    model = whisperx.load_model("large-v2", device, compute_type="float32")

    logging.info("Transcribing audio")
    try:
        transcribe_result = model.transcribe(audio, batch_size=batch_size)
    except Exception as e:
        logging.error(f"Error in transcribing audio: {str(e)}", exc_info=True)
        return {"error": str(e)}

    # delete model if low on GPU resources
    del model
    gc.collect()
    torch.cuda.empty_cache()
    logging.info("Whisper model deleted and GPU cache cleared")

    # 2. Align whisper output
    logging.info("Loading alignment model")
    model_a, metadata = whisperx.load_align_model(language_code=transcribe_result["language"], device=device)
    logging.info("Aligning transcription")
    alignment_result = whisperx.align(transcribe_result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # delete model if low on GPU resources
    del model_a
    gc.collect()
    torch.cuda.empty_cache()
    logging.info("Alignment model deleted and GPU cache cleared")

    word_timings = []

    logging.info("Processing word timings")
    word_segments = alignment_result["word_segments"]
    string_index = 0
    for i, (word_1_info, word_2_info) in enumerate(zip(word_segments[:-1], word_segments[1:])):
        gap_duration = word_2_info["start"] - word_1_info["end"]
        word_timings.append({
            "word1": word_1_info,
            "word1_index": i,
            "word1_string_index": string_index,
            "word2": word_2_info,
            "word2_string_index": string_index + len(word_1_info["word"]) + 1,
            "gap_duration": gap_duration,
        })
        # Add current word length and space from next word
        string_index += len(word_1_info["word"]) + 1

    # Pause behavior
    # Pause duration used in https://doi.org/10.1016/j.jcomdis.2022.106214
    DEFAULT_PAUSE_THRESHOLD_SECONDS = 0.2

    def get_pauses(word_timings, pause_threshold = DEFAULT_PAUSE_THRESHOLD_SECONDS):
        return filter(lambda gap: gap["gap_duration"] > pause_threshold, word_timings)

    logging.info("Calculating pauses")
    pauses = list(get_pauses(word_timings))
    logging.info(f"Found {len(pauses)} pauses")

    word_timings_float = np.fromiter((timing["gap_duration"] for timing in word_timings), dtype=np.float32)
    statistical_pause_threshold = np.mean(word_timings_float) + np.std(word_timings_float)
    logging.info(f"Statistical pause threshold: {statistical_pause_threshold}")
    pauses_by_statistical_threshold = list(get_pauses(word_timings, statistical_pause_threshold))
    logging.info(f"Found {len(pauses_by_statistical_threshold)} pauses using statistical threshold")

    logging.info("Loading spaCy model")
    nlp = spacy.load("en_core_web_sm")

    def get_words(result):
        for segment in result["segments"]:
            for word in segment["words"]:
                yield word["word"]

    full_transcript = " ".join(get_words(alignment_result)).strip()
    logging.info(f"Full transcript length: {len(full_transcript)} characters")

    logging.info("Processing transcript with spaCy")
    doc = nlp(full_transcript)

    logging.info("Analyzing pauses by part of speech")
    pauses_part_of_speech = defaultdict(int)
    pause_index = 0

    for i, token in enumerate(doc):
        if token.idx == pauses[pause_index]["word2_string_index"]:
            pauses_part_of_speech[token.pos_] += 1
            pause_index += 1
            if pause_index >= len(pauses):
                break

    pauses_part_of_speech_rate = {
        key: value / len(pauses) for key, value in pauses_part_of_speech.items()
    }
    logging.info(f"Pause part of speech rates: {pauses_part_of_speech_rate}")

    logging.info("Analyzing sentence-initial pauses")
    sentence_start_indices_set = set(sentence[0].idx for sentence in doc.sents)
    sentence_start_pauses = sum(1 for pause in pauses if pause["word1_string_index"] in sentence_start_indices_set)
    logging.info(f"Number of sentence-initial pauses: {sentence_start_pauses}")

    logging.info("Finding clauses")
    clause_char_spans = []
    added_verb_indices = set()
    for token in doc:
        if token.pos_ != "VERB" or token.i in added_verb_indices:
            continue
        added_verb_indices.add(token.i)
        clause_start = next(token.lefts)

        clause_end = token
        for right_token in token.rights:
            if right_token.pos_ == "VERB":
                if any(right_token_left.dep_ == "nsubj" for right_token_left in right_token.lefts):
                    break
                added_verb_indices.add(right_token.i)
            clause_end = right_token
        clause_char_spans.append((clause_start.idx, clause_end.idx + len(clause_end)))
    logging.info(f"Number of clauses found: {len(clause_char_spans)}")

    logging.info("Analyzing clause-initial pauses")
    clause_start_char_indices = set(span[0] for span in clause_char_spans)
    clause_initial_pause_count = sum(1 for pause in pauses if pause["word1_string_index"] in clause_start_char_indices)
    logging.info(f"Number of clause-initial pauses: {clause_initial_pause_count}")

    logging.info("Pausing behavior analysis completed")
    doc_serializable = [
        {"text": token.text, "pos_": token.pos_, "idx": token.idx}
        for token in doc
    ]
    
    result = {
        "transcription_text": transcribe_result.get('text', ''),
        "alignment_segments": alignment_result.get('segments', []),
        "doc": doc_serializable,
        "pauses": pauses,
        "pauses_by_statistical_threshold": pauses_by_statistical_threshold,
        "pause_part_of_speech_rate": pauses_part_of_speech_rate,
        "clause_char_spans": clause_char_spans,
        "clause_initial_pause_count": clause_initial_pause_count,
    }
    
    return result
    # return {
    #     "transcription_result": transcribe_result,
    #     "doc": doc,
    #     "alignment_result": alignment_result,
    #     "pauses": pauses,
    #     "pauses_by_statistical_threshold": pauses_by_statistical_threshold,
    #     "pause_part_of_speech_rate": pauses_part_of_speech_rate,
    #     "clause_char_spans": clause_char_spans,
    #     "clause_initial_pause_count": clause_initial_pause_count,
    # }

@app.route('/ngram_repetition', methods=['POST'])
def ngram_repetition():
    # Get the text and max_ngram from the request
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    max_ngram = data.get('max_ngram', 3)  # Default to 3 if not provided

    try:
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())

        words = text.split()
        duplicates = []

        for window_size in range(1, max_ngram + 1):
            for i in range(len(words) - 2 * window_size + 1):
                window1 = tuple(words[i:i + window_size])
                window2 = tuple(words[i + window_size:i + 2 * window_size])
                if window1 == window2:
                    duplicates.append({
                        'phrase': ' '.join(window1),
                        'position': i
                    })

        return jsonify({
            'duplicates': duplicates,
            'total_duplicates': len(duplicates)
        })

    except Exception as e:
        # Log the error message to the console
        print(f"Error in ngram_repetition: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/repetitiveness', methods=['POST'])
def repetitiveness():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        # Split text into clauses
        clauses = [clause.strip() for clause in text.split('.') if clause.strip()]

        # Embed the text
        embeddings_matrix = embed_text(clauses, tokenizer, model)

        total_similarity = 0
        count = 0

        while embeddings_matrix.shape[0] > 1:
            root_clause = embeddings_matrix[0:1]  # Keep as 2D array
            embeddings_matrix = embeddings_matrix[1:]

            # Calculate cosine similarities
            similarities = cosine_similarity(embeddings_matrix, root_clause).flatten()

            # Update total similarity and count
            total_similarity += np.sum(similarities)
            count += similarities.shape[0]

        average_similarity = total_similarity / count if count > 0 else 0

        result = {
            'average_similarity': float(average_similarity),
            'total_comparisons': count,
            'num_clauses': len(clauses)
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in repetitiveness: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/lexical_diversity', methods=['POST'])
def lexical_diversity():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        doc = nlp(text)
        words_tagged = [tok.norm_ + "_" + tok.pos_ for tok in doc if tok.pos_ != "PUNCT"]
        ldvals = ld.lexdiv(words_tagged)

        result = {
            'ttr': ldvals.ttr,
            'mattr': ldvals.mattr,
            'hdd': ldvals.hdd
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in lexical_diversity: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/brunet_index', methods=['POST'])
def brunet_index():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        tokens = word_tokenize(text)
        words = [token for token in tokens if re.match(r"^\w.*", token)]

        unique_word_count = len(set(words))
        total_word_count = len(words)

        brunet_index_value = total_word_count ** (unique_word_count ** -0.165)

        result = {
            'brunet_index': brunet_index_value,
            'total_words': total_word_count,
            'unique_words': unique_word_count
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in brunet_index: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/honore_index', methods=['POST'])
def honore_index():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        tokens = word_tokenize(text)
        words = [token for token in tokens if re.match(r"^\w.*", token)]

        _, counts = np.unique(words, return_counts=True)
        honore_index_value = np.sum(counts == 1)

        total_word_count = len(words)
        unique_word_count = len(set(words))

        result = {
            'honore_index': int(honore_index_value),  # Convert to int for JSON serialization
            'total_words': total_word_count,
            'unique_words': unique_word_count
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in honore_index: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/action_verb_rate', methods=['POST'])
def calculate_action_verb_rate():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        rate = action_verb_rate(text)

        result = {
            'action_verb_rate': rate,
            'total_tokens': len(nlp(text)),
            'action_verbs': sum(1 for token in nlp(text) if token.pos_ == "VERB" and is_action_verb(token.text))
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in action_verb_rate: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/negative_adverb_rate', methods=['POST'])
def calculate_negative_adverb_rate():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        rate = negative_adverb_rate(text)

        doc = nlp(text)
        total_tokens = sum(1 for token in doc if token.pos_ != "PUNCT")
        negative_adverbs = sum(1 for token in doc if token.pos_ in ("ADV", "CCONJ") and is_negative_adverb(token.text))

        result = {
            'negative_adverb_rate': rate,
            'total_tokens': total_tokens,
            'negative_adverbs': negative_adverbs
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in negative_adverb_rate: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/part_of_speech_rate', methods=['POST'])
def calculate_part_of_speech_rate():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        doc = nlp(text.strip())
        part_of_speech_counts = Counter(token.pos_ for token in doc if not token.is_stop)
        total_tokens = sum(part_of_speech_counts.values())

        result = {
            'part_of_speech_rates': {pos: count / total_tokens for pos, count in part_of_speech_counts.items()},
            'total_tokens': total_tokens,
            'part_of_speech_counts': dict(part_of_speech_counts)
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in part_of_speech_rate: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/pausing_behavior', methods=['POST'])
def calculate_pausing_behavior():
    data = request.json
    if not data or 'audio_path' not in data:
        return jsonify({'error': 'No audio path provided'}), 400

    audio_path = data['audio_path']
    device = data.get('device', 'cpu')

    try:
        logging.info(f"Loading audio file: {audio_path}")
        
        # Load audio file using librosa
        samples, sr = librosa.load(audio_path, sr=16000, mono=True)
        logging.info("Audio file loaded successfully")

        # Ensure 16kHz sample rate (librosa.load already does this)
        logging.info("Audio loaded at 16kHz and mono")

        # Convert to float32 if not already (librosa.load typically returns float32)
        samples = samples.astype(np.float32)
        logging.info("Audio samples confirmed as float32")
        print(samples)

        logging.info(f"Calculating pausing behavior using device: {device}")
        result = pausing_behavior(samples, device)
        logging.info("Pausing behavior calculation completed")

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in calculate_pausing_behavior: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)