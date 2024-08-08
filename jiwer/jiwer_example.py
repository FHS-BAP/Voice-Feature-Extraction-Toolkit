from jiwer import wer, mer, wil, wip, cer
"""
Jiwer can be used to compare a transcription to a known accurate transcript
to determine its accuracy on the following metrics:
word error rate (WER)
match error rate (MER)
word information lost (WIL)
word information preserved (WIP)
character error rate (CER)
"""
ref_txt = open("manual_transcript.txt", "r")
reference = ref_txt.read()
hypo_txt = open("auto_transcript.txt", "r")
hypothesis = hypo_txt.read()

metrics = {}
metrics['WER'] = wer(reference, hypothesis)
metrics['MER'] = mer(reference, hypothesis)
metrics['WIL'] = wil(reference, hypothesis)
metrics['WIP'] = wip(reference, hypothesis)
metrics['CER'] = cer(reference, hypothesis)

for metric_name, metric in metrics.items():
    print(metric_name, metric)

