from flask import Flask, request, jsonify
import spacy
import sys

app = Flask(__name__)

# Load the English language model
nlp = spacy.load("en_core_web_sm")

@app.route('/tokenize', methods=['POST'])
def tokenize():
    # Get the text from the request
    text = request.json['text']

    # Process the text
    doc = nlp(text)

    # Get the tokens
    try:
        tokens = [token.text for token in doc]
        return jsonify({'tokens': tokens})
    except Exception as e:
        # Log the error message to the console
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/pos_tag', methods=['POST'])
def pos_tag():
    # Get the text from the request
    text = request.json['text']

    # Process the text
    doc = nlp(text)

    # Get the POS tags
    try:
        pos_tags = [(token.text, token.pos_) for token in doc]
        return jsonify({'pos_tags': pos_tags})
    except Exception as e:
        # Log the error message to the console
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/dep_parse', methods=['POST'])
def dep_parse():
    # Get the text from the request
    text = request.json['text']

    # Process the text
    doc = nlp(text)

    # Get the dependency parse
    try:
        dep_parse = [(token.text, token.dep_) for token in doc]
        return jsonify({'dep_parse': dep_parse})
    except Exception as e:
        # Log the error message to the console
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/lemmatize', methods=['POST'])
def lemmatize():
    # Get the text from the request
    text = request.json['text']
    # Process the text
    doc = nlp(text)
    # Get the lemmas
    try:
        lemmas = [token.lemma_ for token in doc]
        return jsonify({'lemmas': lemmas})
    except Exception as e:
        # Log the error message to the console
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/sbd', methods=['POST'])
def sentence_boundary_detection():
    # Get the text from the request
    text = request.json['text']
    # Process the text
    doc = nlp(text)
    # Get the sentence boundaries
    try:
        sentences = [sent.text for sent in doc.sents]
        return jsonify({'sentences': sentences})
    except Exception as e:
        # Log the error message to the console
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/ner', methods=['POST'])
def named_entity_recognition():
    # Get the text from the request
    text = request.json['text']
    # Process the text
    doc = nlp(text)
    # Get the named entities
    try:
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return jsonify({'entities': entities})
    except Exception as e:
        # Log the error message to the console
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)