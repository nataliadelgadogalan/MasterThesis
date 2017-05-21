from os import listdir
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm, neighbors, tree


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
	scoreKnn = clf.score(X_test, y_test)

def compareResultExpected(response, expected):
	sum = 0.0
	for i in range(0, len(response)):
		if response[i] == expected[i]: sum += 1

	percentage = (sum/len(response))*100

	return percentage

def write_csv(data, filname):
	with open(filname, 'wb') as f:
		writer = csv.writer(f)
		for line in data: writer.writerow(line)

def subjectsAverage(path):
	all_results = np.zeros((3,5))
	newpath = path + 'Results/'
	listOfResults = listdir(newpath)
	for result in listOfResults:
		with open(newpath + result) as f:
			reader = csv.reader(f)
			for line in reader: data_temp.append(line)
		all_results = all_results + data_temp

	averageResult = all_results/7
	return averageResult




##### START CODE ################################

listOfSubjects = listdir(path + 'Data/')


#For each subject...
for subject in listOfSubjects:
	newpath = path + 'Data/' + subject + '/'
	listOfStimuliClass = listdir(newpath)
	print 'Subject ' + subject [7]
	EEG_Expected_score = np.zeros((3,5))
	EEG_Response_score = np.zeros((3,5))

	Response_vs_Expected = np.zeros(5)

	# For each stimuli class...
	for stimuli_class in listOfStimuliClass:

		# Read features and data to be classified (all contained in same file)
		attribute_names, attributes, expected, response = readfile(newpath + stimuli_class)

		#Feature normalization


		# classification with SVM
		EEG_Expected_score[0, int(stimuli_class[20])-1] = SVM_classification(attributes = attributes,  target = expected)
		EEG_Response_score[0, int(stimuli_class[20])-1] = SVM_classification(attributes = attributes,  target = response)
		

		# Classification with knn
		EEG_Expected_score[1, int(stimuli_class[20])-1] = knn_classification(attributes = attributes,  target = expected)
		EEG_Response_score[1, int(stimuli_class[20])-1] = knn_classification(attributes = attributes,  target = response)

		#Classification with decision tree
		EEG_Expected_score[2, int(stimuli_class[20])-1] = Dtree_classification(attributes = attributes,  target = expected)
		EEG_Response_score[2, int(stimuli_class[20])-1] = Dtree_classification(attributes = attributes,  target = response)

		# Expected vs Response
		Response_vs_Expected[int(stimuli_class[20])-1] = compareResultExpected(response = response, expected = expected)
	print Response_vs_Expected

	write_csv(EEG_Expected_score, path + 'Results/'+ 'EEG_Expected/' + subject[7] + 'EEG_Expected.csv')
	write_csv(EEG_Response_score, path + 'Results/' + 'EEG_Response/' + subject[7]+'EEG_Response.csv')
	#write_csv(Response_vs_Expected, path + 'Results/' + 'Response_vs_Expected/' + subject[7] + 'Response_vs_Expected.csv')

# Compute average
averageResult = subjectsAverage(path)
print averageResult







