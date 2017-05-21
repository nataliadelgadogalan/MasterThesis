from os import listdir
import csv
import numpy as np
from sklearn import svm, datasets, feature_selection
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

path = 'C:/Users/natad/Documents/SMC/MasterThesis/CORRELATIONS/'
listOfVideos = listdir(path + 'AudioFeatures/')


# To change depending on number of feature types (4), number of features per type desired (3) [3*4=12]
# and number of subjects (7)
final_features = [['']*8 for i in range(12)]

print final_features
final_features[3][2] = 'ueeee'
final_features[4][1] = 'aaaa'
print final_features
n_audiofeatures = 3
output_name = 'SelectedFeatures_Typical.csv'
# It is also recommended to name files as in the example, so that further naming of files fit


#####################FUNCTIONS #############

def readfile(filename):
		data_temp = []
		with open(filename) as f:
			reader = csv.reader(f)
			for line in reader: data_temp.append(line)

		names = data_temp[0]
		data = np.array(data_temp[1:], dtype=np.float32)

		return names, data

def ranker(X, y, n_features):

	X_aux = SelectKBest(f_classif, k=n_features)
	Selected = X_aux.fit_transform(X,y)
	indexes = X_aux.get_support(indices=True)

	return indexes


def arousalValenceRanker(audio_feature, eeg_feature,  n_features):
	# Feature ranking (arousal)
	y = eeg_feature[:,1]
	arousal_indexes = ranker(X = audio_feature, y=y, n_features=n_features)
	


	# Feature ranking (valence)
	y = eeg_feature[:,5]
	valence_indexes = ranker(audio_feature, y, n_features)
	


	# Select three first features in the intersection between valence and arousal
	#inters = X_valence.intersection(X_arousal)
	inters = list(set(arousal_indexes) & set(valence_indexes))

	return inters





##################### START CODE ########################################
list_of_subjects = []
list_of_featureTypes = []
# for: video1 + video 2
for video in listOfVideos:
	# intialize counter for each video, to store data in correct positions
	feature_counter = -3
	print 'VIDEO: ' + video
	newpath = path + 'AudioFeatures/' + video + '/'
	listOfFeatures = listdir(newpath)
	listOfEEGFiles = listdir(path + 'EEGFeatures/' + video + '/')

	# for all four types of features
	for file in listOfFeatures:
		
		print file
		feature_counter += 3

		#fill in feature name for final csv
		for i in range (0,3):
				final_features[feature_counter + i][0] = file[:-4]


		# read set of selected features (timbre, melody, harmony, rhythm)
		AFeature_names, audio_feature = readfile(newpath + file)
		list_of_featureTypes.append(file[:-4])


		# For all subjects in video folder
		for EEGfile in listOfEEGFiles:
			n_features = 5
			print EEGfile
			# Read EEG data
			EEGFeature_names, eeg_feature = readfile(path + 'EEGFeatures/' + video + '/' + EEGfile)

			# Arousal and Valence Ranking
			y = eeg_feature[:,1]

			indexes = arousalValenceRanker(audio_feature= audio_feature, eeg_feature = eeg_feature,  n_features = n_features)
			rows = audio_feature.shape
			print 'rows'
			rows = rows[1]
			print rows
			# to avoid searching for too many or too few features, k is initialised at 5 and increased in not enough have been found
			while len(indexes) < 3:
				indexes = arousalValenceRanker(audio_feature= audio_feature, eeg_feature = eeg_feature,  n_features = n_features)
				n_features += np.ceil(0.01*rows)
				# to avoid selecting more attributes than existing...
				if n_features > rows: n_features = rows 

			# Store in matrix features corresponding to the indexes 
			for i in range (0,3):
				final_features[feature_counter + i][int(EEGfile[7])] = AFeature_names[indexes[i]]
			#final_features[feature_counter : feature_counter+3, int(EEGfile[7])-1] = indexes[0:3]


	 		print final_features

 	 		


 # Save features per subject in a csv
#with open(path + 'SelectedFeatures/' + output_name , 'wb') as f:
with open('output.csv', 'wb') as f:
	writer = csv.writer(f)
	first_line = [' ', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5','Subject 6','Subject 7']
	writer.writerow(first_line)
	for line in final_features:
		writer.writerow(line)

		


# Hacer buena clasificación de los low level features
# Comprobar que estos features tienen sentido

# Hacer classification: svm, knn, ...

# Hacer correlacion