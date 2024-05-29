"""
run.py
generate OSM features on WAV files;
"""
from osm import extract_osm_features

def extract_llds():
	"""
	extract low level descriptiors
	"""
	audio_fp = 'sample_wav/first_ten_Sample_HV_Clip.wav'
	csv_out = 'sample_out/first_ten_Sample_HV_Clip_lld.csv'
	extract_osm_features(audio_fp, csv_out, feat_level='lld')

def extract_functionals():
	"""
	extract functionals
	"""
	audio_fp = 'sample_wav/first_ten_Sample_HV_Clip.wav'
	csv_out = 'sample_out/first_ten_Sample_HV_Clip_functionals.csv'
	extract_osm_features(audio_fp, csv_out, feat_level='functionals')

def main():
	"""
	main entrypoint
	"""
	extract_llds()
	extract_functionals()

if __name__ == '__main__':
	main()
