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
	scoreKnn = clf.score(X_test, y_test)

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
	AgressiveData = []
	CalmData = []
	HappyData = []
	SadData = []

	fig, ax = plt.subplots()
	for i in range (0, size_y[0] ):
		Arousal = eeg_feature[i,1]
		Valence = eeg_feature[i,5]
		answer = expected[i]
		index = [k for k,x in enumerate(legend) if x==answer]
		ax.scatter(Valence, Arousal, color = colours[index[0]])
		ax.set_xlabel('Valence')
		ax.set_ylabel('Arousal')

		if index[0] == 0: AgressiveData.append([Valence, Arousal])
		if index[0] == 1: CalmData.append([Valence, Arousal])
		if index[0] == 2: HappyData.append([Valence, Arousal])
		if index[0] == 3: SadData.append([Valence, Arousal])

	#Plot
	title = 'Arousal-Valence Centroids for' + plotName[-18:-11] + plotName[-10:-4]
	plt.title(title)
	plt.savefig(plotName)


	# Calculate centroid for data:	
	centroidA = computeCentroid(AgressiveData)
	centroidC = computeCentroid(CalmData)
	centroidH = computeCentroid(HappyData)
	centroidS= computeCentroid(SadData)

	# Plot centroids
	fig, ax = plt.subplots()
	ax.scatter(centroidA[0], centroidA[1], color = colours[0])
	ax.scatter(centroidC[0], centroidC[1], color = colours[1])
	ax.scatter(centroidH[0], centroidH[1], color = colours[2])
	ax.scatter(centroidS[0], centroidS[1], color = colours[3])
	ax.set_xlabel('Valence')
	ax.set_ylabel('Arousal')
	#ax.legend(handles=colours, labels = legend)
	title = 'Arousal-Valence Centroids for' + plotName[-18:-11] + plotName[-10:-4]
	plt.title(title)
	plt.savefig(plotName[:-4]+'_centroids.png')
	
	return 

def computeCentroid(data):
	centroid = (sum(data[0])/len(data[0]),sum(data[1])/len(data[1]))
	
	return centroid




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

		# Plot arousal vs valence with expected response, to search for a match
		plot(eeg_feature = attributes, expected = expected, plotName = path +'Plots/'+ subject + '_' + stimuli_class[15:20] + '.png')


	write_csv(EEG_Expected_score, path + 'Results/'+ 'EEG_Expected/' + subject[7] + 'EEG_Expected.csv', average = 0, flag =0)
	write_csv(EEG_Response_score, path + 'Results/' + 'EEG_Response/' + subject[7]+'EEG_Response.csv', average = 0, flag = 0)
	write_csv([Response_vs_Expected], path + 'Results/' + 'Response_vs_Expected/' + subject[7] + 'Response_vs_Expected.csv', average = 0, flag = 0)

# Compute average
# Compute average
newpath = path + 'Results/'
listOfResultFolders = listdir(newpath)
flag = 0

for folder in listOfResultFolders:
	print folder
	if folder == 'Response_vs_Expected': flag = 1
	averageResult = subjectsAverage(newpath + folder+ '/', flag)

write_csv(EEG_Expected_score, path + 'Average_Results/'+ 'Average_EEG_Expected.csv', average = 1, flag = 0)
write_csv(EEG_Response_score, path + 'Average_Results/'  + 'Average_EEG_Response.csv', average = 1, flag = 0)
write_csv([Response_vs_Expected], path + 'Average_Results/' + 'Average_Response_vs_Expected.csv', average = 1, flag = 1)






