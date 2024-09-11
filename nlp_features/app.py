from flask import Flask, request, jsonify
import re
import sys
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy
from taaled import ld
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import sentiwordnet as swn
from transformers import T5Tokenizer, T5ForConditionalGeneration
from collections import Counter

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)