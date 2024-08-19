import transformers
import datasets
import torch

def load(**kwargs):
    processor = transformers.WhisperProcessor.from_pretrained("openai/whisper-base")
    model = transformers.WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")

    tokenizer = processor.tokenizer
    START_OF_TRANSCRIPT_TOKEN = tokenizer.all_special_ids[tokenizer.all_special_tokens.index("<|startoftranscript|>")]

    def transcribe(dataset: datasets.Dataset):
        dataset = dataset.with_format("torch")
        processed_audio = dataset.map(lambda batch: processor(batch["audio"]["array"], sampling_rate=batch["audio"]["sampling_rate"], return_tensors="pt"))
        input_features = torch.tensor(processed_audio["input_features"]).squeeze(1)

        prompt_ids = processor.get_prompt_ids("uh, um, but, like", return_tensors="pt")
        output_tokens = model.generate(input_features, prompt_ids=prompt_ids)

        start_of_transcript_index = output_tokens[0].tolist().index(START_OF_TRANSCRIPT_TOKEN)
        output_tokens = output_tokens[:, start_of_transcript_index:]

        result = processor.batch_decode(output_tokens, skip_special_tokens=True)

        return [{"text": text} for text in result]

    return transcribe