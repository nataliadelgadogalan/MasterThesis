
from scipy.io import wavfile
import essentia
import os
import subprocess
from essentia.standard import *
# as there are 2 operating modes in essentia which have the same algorithms,
# these latter are dispatched into 2 submodules:
import essentia.standard
import essentia.streaming
from os import listdir

#Global parameters
frameLen = 1 # length of frame in seconds
hopLen = 0.09346 # length of hop in seconds
fs = 44100
path = '/home/natalia/Documents/SMC/Thesis/'
output_name = 'Audio_Features_Video2_part3.csv'

# Order of audios in video
#audio_order = ['H1.wav', 'C3.wav', 'S3.wav', 'A3.wav', 'S1.wav', 'H2.wav', 'S2.wav', 'C2.wav', 'C1.wav', 'A1.wav', 'A2.wav', 'H3.wav'] # video 1 part 1
#audio_order = ['H2.wav', 'H3.wav', 'S3.wav', 'A2.wav', 'S1.wav', 'A3.wav', 'H1.wav', 'C1.wav', 'A1.wav', 'S2.wav', 'C2.wav', 'C3.wav'] # video 1 part 2
#audio_order = ['C2.wav', 'H3.wav', 'A3.wav', 'A1.wav', 'S2.wav', 'S3.wav', 'C3.wav', 'C1.wav', 'H1.wav', 'H2.wav', 'S1.wav', 'A2.wav'] # video 1 part 3
#audio_order = ['H2.wav', 'H1.wav', 'S3.wav', 'A2.wav', 'C2.wav', 'H3.wav', 'C3.wav', 'C1.wav', 'A3.wav', 'S1.wav', 'A1.wav', 'S2.wav'] # video 2 part 1
#audio_order = ['A3.wav', 'C2.wav', 'H3.wav', 'S2.wav', 'H1.wav', 'C1.wav', 'A2.wav', 'H2.wav', 'A1.wav', 'S1.wav', 'S3.wav', 'C3.wav'] # video 2 part 2
audio_order = ['H2.wav', 'C2.wav', 'A3.wav', 'S1.wav', 'C3.wav', 'A1.wav', 'S2.wav', 'C1.wav', 'S3.wav', 'H3.wav', 'A2.wav', 'H1.wav'] # video 2 part 3


#Start code
newpath = path + 'AUDIOS/'
listOfAudios = listdir(newpath)
index = 1.0

for k  in range (0,len(listOfAudios)):

	file = audio_order[k]
	print (newpath + file)
	loader = essentia.standard.MonoLoader(filename=newpath+file)

	# and then we actually perform the loading:
	audio = loader()
	audio = audio[0:10*fs]
	print(len(audio))

	frameSize = int(fs*frameLen)
	print frameSize
	hopSize = int(fs*hopLen)
	print hopSize
	counter = 1
	for fstart in range(0, len(audio)-hopSize, hopSize):
		frame = audio[fstart:fstart+frameSize]

		wavfile.write(path + 'test.wav',44100,frame)
		

		args = (path + 'MUSIC_EXTRACTOR/' + 'streaming_extractor_music', path + 'test.wav',  path + 'JSON_FILES/' + str(index) + '.json', "profile.json")
		counter += 1
		index += 0.0001
		popen = subprocess.Popen(args, stdout=subprocess.PIPE)
		popen.wait()
		output = popen.stdout.read()
		print output

	print 'End of file' + file[:-4] + '(' + str(counter) + 'lines)'
		
os.chdir(path + 'FEATURES/')
os.system("python json_to_csv.py -i " + path + "JSON_FILES/*.json -o " + output_name + " --include lowlevel.* lowlevel.average_loudness* lowlevel.dynamic_complexity* lowlevel.dissonance* lowlevel.melbands* lowlevel.barkbands* lowlevel.hfc* lowlevel.pitch_salience* lowlevel.spectral_centroid* lowlevel.spectral_complexity* lowlevel.spectral_decrease* lowlevel.spectral_energy* lowlevel.spectral_energyband_high* lowlevel.spectral_energyband_low* lowlevel.spectral_energyband_middle_high* lowlevel.spectral_energyband_middle_low* lowlevel.spectral_entropy* lowlevel.spectral_flux*lowlevel.spectral_kurtosis* lowlevel.spectral_rms* lowlevel.spectral_rolloff* lowlevel.spectral_skewness* lowlevel.spectral_spread* lowlevel.spectral_strongpeak* lowlevel.zerocrossingrate* lowlevel.mfcc.mean* lowlevel.spectral_contrast_coeffs* lowlevel.spectral_contrast_valleys* rhythm.bpm* rhythm.onset_rate* rhythm.beats_count* rhythm.danceability* tonal.chords_changes_rate* tonal.chords_number_rate* tonal.key_strength* tonal.tuning_diatonic_strength* tonal.tuning_equal_tempered_deviation* tonal.tuning_frequency* tonal.tuning_nontempered_energy_ratio* tonal.chords_strength* tonal.hpcp_entropy* tonal.chords_histogram* tonal.thpcp* tonal.hpcp* tonal.chords_key* tonal.chords_scale* tonal.key_key* tonal.key_scale*")

#python json_to_csv.py -i /home/natalia/Documents/SMC/Thesis/JSON_FILES/*.json -o Audio_Features_Video1_part1.csv --include lowlevel.* lowlevel.average_loudness* lowlevel.dynamic_complexity* lowlevel.dissonance* lowlevel.melbands* lowlevel.barkbands* lowlevel.hfc* lowlevel.pitch_salience* lowlevel.spectral_centroid* lowlevel.spectral_complexity* lowlevel.spectral_decrease* lowlevel.spectral_energy* lowlevel.spectral_energyband_high* lowlevel.spectral_energyband_low* lowlevel.spectral_energyband_middle_high* lowlevel.spectral_energyband_middle_low* lowlevel.spectral_entropy* lowlevel.spectral_flux*lowlevel.spectral_kurtosis* lowlevel.spectral_rms* lowlevel.spectral_rolloff* lowlevel.spectral_skewness* lowlevel.spectral_spread* lowlevel.spectral_strongpeak* lowlevel.zerocrossingrate* lowlevel.mfcc.mean* lowlevel.spectral_contrast_coeffs* lowlevel.spectral_contrast_valleys* rhythm.bpm* rhythm.onset_rate* rhythm.beats_count* rhythm.danceability* tonal.chords_changes_rate* tonal.chords_number_rate* tonal.key_strength* tonal.tuning_diatonic_strength* tonal.tuning_equal_tempered_deviation* tonal.tuning_frequency* tonal.tuning_nontempered_energy_ratio* tonal.chords_strength* tonal.hpcp_entropy* tonal.chords_histogram* tonal.thpcp* tonal.hpcp* tonal.chords_key* tonal.chords_scale* tonal.key_key* tonal.key_scale*")

#python json_to_csv.py -i /home/natalia/Documents/SMC/Thesis/JSON_FILES/*.json -o Audio_Features_Video1_part1.csv --include lowlevel.average_loudness* lowlevel.dynamic_complexity* lowlevel.dissonance* lowlevel.hfc* lowlevel.pitch_salience* lowlevel.spectral_centroid* lowlevel.spectral_complexity* lowlevel.spectral_decrease* lowlevel.spectral_energy* lowlevel.spectral_energyband_high* lowlevel.spectral_energyband_low* lowlevel.spectral_energyband_middle_high* lowlevel.spectral_energyband_middle_low* lowlevel.spectral_entropy* lowlevel.spectral_flux*lowlevel.spectral_kurtosis* lowlevel.spectral_rms* lowlevel.spectral_rolloff* lowlevel.spectral_skewness* lowlevel.spectral_spread* lowlevel.spectral_strongpeak* lowlevel.zerocrossingrate* lowlevel.mfcc.mean* lowlevel.spectral_contrast_coeffs* lowlevel.spectral_contrast_valleys* rhythm.bpm rhythm.onset_rate*   tonal.chords_changes_rate*tonal.chords_number_rate* tonal.key_strength* tonal.tuning_diatonic_strength* tonal.tuning_equal_tempered_deviation* tonal.tuning_frequency* tonal.tuning_nontempered_energy_ratio* tonal.chords_strength* tonal.hpcp_entropy* tonal.chords_histogram* tonal.thpcp* tonal.hpcp* tonal.chords_key* tonal.chords_scale* tonal.key_key* tonal.key_scale*


    

