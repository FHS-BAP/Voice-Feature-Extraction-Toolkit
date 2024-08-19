import transformers

def load():
    transcriber = transformers.pipeline("automatic-speech-recognition", model="NbAiLabBeta/nb-whisper-medium-verbatim", trust_remote_code=True)

    def transcribe_function(dataset):
        return transcriber(dataset["audio"], generate_kwargs={'task': 'transcribe', 'language': 'en'})
    
    return transcribe_function