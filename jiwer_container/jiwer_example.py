from jiwer import wer
"""
Jiwer can be used to compare a transcription to a known accurate transcript
to determine its accuracy on the following metrics:
word error rate (WER)
match error rate (MER)
word information lost (WIL)
word information preserved (WIP)
character error rate (CER)
"""

reference = "hello world"
hypothesis = "hello duck"

error = wer(reference, hypothesis)