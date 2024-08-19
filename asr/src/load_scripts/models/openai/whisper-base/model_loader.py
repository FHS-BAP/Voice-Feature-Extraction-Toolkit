import transformers

def load():
    transcriber = transformers.pipeline("automatic-speech-recognition", model="openai/whisper-base", trust_remote_code=True)
    return lambda dataset: transcriber(dataset["audio"])