from os import listdir
import csv
import numpy as np

path = 'C:/Users/natad/Documents/SMC/MasterThesis/FeatureSelection/'


######### FUNCTIONS######################

def readfile(filename):
		data_temp = []
		with open(filename) as f:
			reader = csv.reader(f)
			for line in reader: data_temp.append(line)

		data = np.array(data_temp, dtype=np.float32)

		return data


########### CODE #####################



listOfFiles = listdir(path + 'SelectedFeatures/')
audioFeatures = readfile(path + 'SelectedFeatures/' + listOfFiles[0])
sizeAF = audioFeatures.shape

for i in range (0, len(listOfFiles), 4):
	AudioFeaturesSelected = np.zeros((sizeAF[0], 12))

	for k in range (0, 4):
		print i+k
		print listOfFiles[i+k]
		audioFeatures = readfile(path + 'SelectedFeatures/' + listOfFiles[i+k])
		AudioFeaturesSelected[:,k*3:(k+1)*3] = audioFeatures

	newFilename = path + 'FinalSelectedFeatures_Typical/' + 'SelectedAudioFeatures_Subject ' + listOfFiles[i+k][0]  +'.csv'
	with open(newFilename, 'wb') as f:
		writer = csv.writer(f)
		for line in AudioFeaturesSelected: writer.writerow(line)

