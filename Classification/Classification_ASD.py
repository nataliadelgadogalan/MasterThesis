from os import listdir
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm, neighbors, tree
import matplotlib.pyplot as plt


path  = 'C:/Users/natad/Documents/SMC/MasterThesis/DataPostprocessing/Classification/'

###### FUNCTIONS #######################

def readfile(filename):

		data_temp = []
		expected = []
		response = []

		firstline = True
		with open(filename) as f:
			reader = csv.reader(f)
			for line in reader: 
				if firstline:    #skip first line
					firstline = False
					continue
				data_temp.append(line[:-2])
				expected.append(line[-2])
				response.append(line[-1])

		names = data_temp[0]
		attributes = np.array(data_temp, dtype=np.float32)

		return names, attributes, expected, response 

def SVM_classification(attributes, target):
	X_train, X_test, y_train, y_test = train_test_split(attributes, target, test_size=0.25, random_state=0)
	#svc parameters by default 
	clf = svm.SVC(C=1.0, kernel='poly', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None).fit(X_train, y_train)
	scoreSVM = clf.score(X_test, y_test)

	return scoreSVM

def knn_classification(attributes, target):
	X_train, X_test, y_train, y_test = train_test_split(attributes, target, test_size=0.25, random_state=0)
	knn = neighbors.KNeighborsClassifier().fit(X_train, y_train)
	scoreKnn = knn.score(X_test, y_test)

	return scoreKnn

def Dtree_classification(attributes, target):
	X_train, X_test, y_train, y_test = train_test_split(attributes, target, test_size=0.25, random_state=0)
	clf = tree.DecisionTreeClassifier().fit(X_train, y_train)
	scoreDT = clf.score(X_test, y_test)

	return scoreDT

def compareResultExpected(response, expected):
	sum = 0.0
	for i in range(0, len(response)):
		if response[i] == expected[i]: sum += 1

	percentage = (sum/len(response))*100

	return percentage

def write_csv(data, filname, average, flag):
	ML = ['SVM', 'kNN', 'DT']
	with open(filname, 'wb') as f:
		writer = csv.writer(f)

		if average == 1:
			first_line = [' ', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5']
			writer.writerow(first_line)
			count = 0

			for line in data:
				if flag == 1: newline = ['Average Score' , line[0], line[1], line[2], line[3], line[4]]
				else: newline = [ML[count] , line[0], line[1], line[2], line[3], line[4]]
				writer.writerow(newline)
				count += 1

		else:		
			for line in data: writer.writerow(line)

def subjectsAverage(path, flag):
	print path
	if flag == 1: all_results = np.zeros(5)
	else: all_results = np.zeros((3,5))
	print 'PATHH'
	print path
	listOfResults = listdir(path)
	print 'list of resuls:'
	print listOfResults

	for result in listOfResults:
		print result
		data_temp = []
		with open(path + result) as f:
			reader = csv.reader(f)
			for line in reader: data_temp.append(line)

		print data_temp
		print np.array(data_temp, dtype=np.float32)
		all_results = all_results + np.array(data_temp, dtype=np.float32)

	averageResult = all_results/7
	return averageResult



def plot(eeg_feature, expected, plotName):
	size_y = eeg_feature.shape
	legend = ['Agressive', 'Calm', 'Happy', 'Sad']
	colours = ['r', 'b', 'c', 'g']
	AgressiveDataA = []
	CalmDataA = []
	HappyDataA = []
	SadDataA = []
	AgressiveDataV = []
	CalmDataV = []
	HappyDataV = []
	SadDataV = []

	#fig, ax = plt.subplots()
	for i in range (0, size_y[0] ):
		Arousal = eeg_feature[i,1]
		Valence = eeg_feature[i,5]
		answer = expected[i]
		index = [k for k,x in enumerate(legend) if x==answer]
		#ax.scatter(Valence, Arousal, color = colours[index[0]])
		#ax.set_xlabel('Valence')
		#ax.set_ylabel('Arousal')

		if index[0] == 0: 
			AgressiveDataA.append(Arousal)
			AgressiveDataV.append(Valence)
		if index[0] == 1: 
			CalmDataA.append(Arousal)
			CalmDataV.append(Valence)
		if index[0] == 2: 
			HappyDataA.append(Arousal)
			HappyDataV.append(Valence)
		if index[0] == 3: 
			SadDataA.append(Arousal)
			SadDataV.append(Valence)


	#Plot
	#title = 'Arousal-Valence Centroids for' + plotName[-19:-11] + plotName[-10:-4]
	#plt.title(title)
	#plt.savefig(plotName)


	# Calculate centroid for data:	
	centroidAA, centroidAV = computeCentroid(AgressiveDataA, AgressiveDataV, type = 0)
	centroidCA, centroidCV = computeCentroid(CalmDataA, CalmDataV, type = 0)
	centroidHA, centroidHV = computeCentroid(HappyDataA, HappyDataV, type = 0)
	centroidSA, centroidSV = computeCentroid(SadDataA, SadDataV, type = 0)

	# Plot centroids
	# fig, ax = plt.subplots()
	# ax.scatter(centroidAA, centroidAV, color = colours[0])
	# ax.scatter(centroidCA, centroidCV, color = colours[1])
	# ax.scatter(centroidHA, centroidHV, color = colours[2])
	# ax.scatter(centroidSA, centroidSV, color = colours[3])
	# ax.set_xlabel('Valence')
	# ax.set_ylabel('Arousal')
	# #ax.legend(handles=colours, labels = legend)
	# title = 'Arousal-Valence Centroids for ' + plotName[-19:-11] +','+ plotName[-10:-4]
	# plt.title(title)
	# plt.savefig(plotName[:-4]+'_centroids.png')
	
	return AgressiveDataA, AgressiveDataV, CalmDataA, CalmDataV, HappyDataA, HappyDataV, SadDataA, SadDataV

def computeCentroid(data1, data2, type):
	
	
	if type == 0:
		data1 = np.array(data1, dtype=np.float32)
		data2 = np.array(data2, dtype=np.float32)
		centroidA = sum(data1)/len(data1)
		centroidV = sum(data2)/len(data2)
	if type == 1:
		s = len(data1)
		lenData1 = 0
		sumData1 = 0
		lenData2 = 0
		sumData2 = 0
		for i in range (0, len(data1)):
			data1_aux = np.array(data1[i], dtype=np.float32)
			data2_aux = np.array(data2[i], dtype=np.float32)
			lenData1 += len(data1_aux)
			sumData1 += sum(data1_aux)
			lenData2 += len(data2_aux)
			sumData2 += sum(data2_aux)


		centroidA = sumData1/lenData1
		centroidV = sumData2/lenData2

	return centroidA, centroidV

def normalize(data):
	norm = (data - min(data))/(max(data)-min(data))

	return norm

def tuple_to_array(data):
	data1 = [(tup[0],) for tup in data]
	data1 = np.array(data1, dtype=np.float32)
	data2 = [(tup[1],) for tup in data]
	data2 = np.array(data2, dtype=np.float32)

	return data1, data2


##### START CODE ################################

listOfSubjects = listdir(path + 'Data_ASD/')
Classes = ['Audio', 'Visual', 'Coh_Audio-Visual', 'inc_Audio-Visual_A', 'inc_Audio-Visual_V']
AgressiveAFinal = []
CalmAFinal = []
HappyAFinal = []
SadAFinal = []
AgressiveVFinal = []
CalmVFinal = []
HappyVFinal = []
SadVFinal = []

#For each subject...
for subject in listOfSubjects:
	newpath = path + 'Data_ASD/' + subject + '/'
	listOfStimuliClass = listdir(newpath)
	print 'Subject ' + subject [3]
	EEG_Expected_score = np.zeros((3,5))
	EEG_Response_score = np.zeros((3,5))

	Response_vs_Expected = np.zeros(5)

	# For each stimuli class...
	for stimuli_class in listOfStimuliClass:

		# Read features and data to be classified (all contained in same file)
		attribute_names, attributes, expected, response = readfile(newpath + stimuli_class)

		#Feature normalization


		# classification with SVM
		EEG_Expected_score[0, int(stimuli_class[10])-1] = SVM_classification(attributes = attributes,  target = expected)
		EEG_Response_score[0, int(stimuli_class[10])-1] = SVM_classification(attributes = attributes,  target = response)
		

		# Classification with knn
		EEG_Expected_score[1, int(stimuli_class[10])-1] = knn_classification(attributes = attributes,  target = expected)
		EEG_Response_score[1, int(stimuli_class[10])-1] = knn_classification(attributes = attributes,  target = response)

		#Classification with decision tree
		EEG_Expected_score[2, int(stimuli_class[10])-1] = Dtree_classification(attributes = attributes,  target = expected)
		EEG_Response_score[2, int(stimuli_class[10])-1] = Dtree_classification(attributes = attributes,  target = response)

		# Expected vs Response
		Response_vs_Expected[int(stimuli_class[10])-1] = compareResultExpected(response = response, expected = expected)

		# Plot arousal vs valence with expected response, to search for a match
		print stimuli_class[10]
		AgressiveDataA, AgressiveDataV, CalmDataA, CalmDataV, HappyDataA, HappyDataV, SadDataA, SadDataV= plot(eeg_feature = attributes, expected = expected, plotName = path +'Plots/'+ subject + '_' + Classes[int(stimuli_class[10])-1]+ '.png')
		
		# To plot average of one of classes of each subject
		if int(stimuli_class[10]) == 1:
			aggressiveDA = normalize(AgressiveDataA)
			aggressiveDV = normalize(AgressiveDataV)
			calmDA = normalize(CalmDataA)
			calmDV = normalize(CalmDataV)
			HappyDA = normalize(HappyDataA)
			HappyDV = normalize(HappyDataV)
			SadDA = normalize(SadDataA)
			SadDataV = normalize(SadDataV)

			AgressiveAFinal.append(aggressiveDA)
			AgressiveVFinal.append(aggressiveDV)
			CalmAFinal.append(calmDA)
			CalmVFinal.append(calmDV)
			HappyAFinal.append(HappyDA)
			HappyVFinal.append(HappyDV)
			SadAFinal.append(SadDA)
			SadAFinal.append(SadDA)

	# Store average data
	write_csv(EEG_Expected_score, path + 'Results_ASD/'+ 'EEG_Expected/' + subject[3] + 'EEG_Expected.csv', average = 0, flag =0)
	write_csv(EEG_Response_score, path + 'Results_ASD/' + 'EEG_Response/' + subject[3]+'EEG_Response.csv', average = 0, flag = 0)
	write_csv([Response_vs_Expected], path + 'Results_ASD/' + 'Response_vs_Expected/' + subject[3] + 'Response_vs_Expected.csv', average = 0, flag = 0)


#print AgressiveFinal
print AgressiveAFinal
centroidAA, centroidAV = computeCentroid(AgressiveAFinal, AgressiveVFinal, type = 1)
centroidCA, centroidCV = computeCentroid(CalmAFinal, CalmVFinal, type = 1)
centroidHA, centroidHV = computeCentroid(HappyAFinal, HappyVFinal, type = 1)
centroidSA, centroidSV = computeCentroid(SadAFinal, SadAFinal, type = 1)

print centroidAA, centroidAV

# Plot average for one class
fig, ax = plt.subplots()
ax.scatter(centroidAA, centroidAV, color = 'r')
ax.scatter(centroidCA, centroidCV, color = 'b')
ax.scatter(centroidHA, centroidHV, color = 'c')
ax.scatter(centroidSA, centroidSV, color = 'g')
ax.set_xlabel('Valence')
ax.set_ylabel('Arousal')

title = 'Average Arousal-Valence Centroids for Audio Stimuli'
plt.title(title)
plt.savefig(path +'Plots_ASD/'+ 'CentroidsAV_class1.png')

	
# Compute average
# Compute average
newpath = path + 'Results_ASD/'
listOfResultFolders = listdir(newpath)
flag = 0

for folder in listOfResultFolders:
	print folder
	if folder == 'Response_vs_Expected': flag = 1
	averageResult = subjectsAverage(newpath + folder+ '/', flag)

write_csv(EEG_Expected_score, path + 'Average_Results_ASD/'+ 'Average_EEG_Expected.csv', average = 1, flag = 0)
write_csv(EEG_Response_score, path + 'Average_Results_ASD/'  + 'Average_EEG_Response.csv', average = 1, flag = 0)
write_csv([Response_vs_Expected], path + 'Average_Results_ASD/' + 'Average_Response_vs_Expected.csv', average = 1, flag = 1)






