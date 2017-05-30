from os import listdir
import csv
import numpy as np
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import seaborn as sns

path = 'C:/Users/natad/Documents/SMC/MasterThesis/DataPostprocessing/ConfusionMatrix/'


######### FUNCTIONS######################

def readfile(filename):
		expected = []
		response = []

		firstline = True
		with open(filename) as f:
			reader = csv.reader(f)
			for line in reader: 
				if firstline:    #skip first line
					firstline = False
					continue
				expected.append(line[-2])
				response.append(line[-1])


		return expected, response 



def confusionMatrix(response, expected):
	labels = ['Agressive', 'Calm', 'Happy', 'Sad', '?', '']
	confMatrix = np.zeros((4,4))

	for i in range(0, len(response)):
		R = labels.index(response[i])
		E = labels.index(expected[i])
		if R < 4: confMatrix[R,E] += 1

	return confMatrix

def normalizeMatrix(confMatrix):
	newConfMatrix = np.zeros((4,4))
	for i in range (0,4):
		maxX = max(confMatrix[:,i])
		minX = min(confMatrix[:,i])
		newConfMatrix[:,i] = (confMatrix[:,i] - minX) / (maxX -minX)

	return newConfMatrix


def plotMatrix(confMatrix, plotName):
	fig, ax = plt.subplots()
	labels = ['Agressive', 'Calm', 'Happy', 'Sad']
	ax = sns.heatmap(confMatrix)
	ax.set_ylabel('Response')
	ax.set_xlabel('Expected Response')
	plt.xticks(range(0,4),labels)
	plt.yticks(range(0,4),labels[::-1])
	title = 'Confusion Matrix for Typical Subjects: ' + plotName[85:-4]
	plt.title(title)
	#sns.plt.show()
	#fig = ax.get_figure()
	#fig.savefig(plotName)
	plt.savefig(plotName)




########### CODE #####################

listOfSubjects = listdir(path + 'DataT/')
averageConfMatrix_audio = np.zeros((4,4))
averageConfMatrix_visual = np.zeros((4,4))
averageConfMatrix_AV_C = np.zeros((4,4))
averageConfMatrix_AV_NC_A = np.zeros((4,4))
averageConfMatrix_AV_NC_V = np.zeros((4,4))
Classes = ['Audio', 'Visual', 'C_Audio-Visual', 'NC_Audio-Visual_A' , 'NC_Audio-Visual_V']

#For each subject...
for subject in listOfSubjects:
	newpath = path + 'DataT/' + subject + '/'
	listOfStimuliClass = listdir(newpath)

	# For each stimuli class...
	for stimuli_class in listOfStimuliClass:
		#Read features and data to be classified (all contained in same file)
		expected, response = readfile(newpath + stimuli_class)
		confMatrix = confusionMatrix(response, expected)
		print confMatrix
		#normConfMatrix = normalize(confMatrix, norm = 'l1', axis = 0)
		
		normConfMatrix = normalizeMatrix(confMatrix)
		print normConfMatrix
		plotMatrix(normConfMatrix, plotName = path + 'OutputT/Subject' + subject[7] + '_' + Classes[int(stimuli_class[20])-1] + '.png')

		# add values to average matrix
		if int(stimuli_class[20]) == 1: averageConfMatrix_audio = averageConfMatrix_audio + confMatrix
		if int(stimuli_class[20]) == 2: averageConfMatrix_visual = averageConfMatrix_visual + confMatrix
		if int(stimuli_class[20]) == 3: averageConfMatrix_AV_C = averageConfMatrix_AV_C + confMatrix
		if int(stimuli_class[20]) == 4: averageConfMatrix_AV_NC_A = averageConfMatrix_AV_NC_A + confMatrix
		if int(stimuli_class[20]) == 5: averageConfMatrix_AV_NC_V = averageConfMatrix_AV_NC_V + confMatrix
		

#normalize and plot average matrix
normConfMatrix = normalizeMatrix(averageConfMatrix_audio)
#normConfMatrix = normalize(averageConfMatrix_audio, norm = 'l1', axis = 0)
plotMatrix(averageConfMatrix_audio, plotName = path + 'OutputT/Average_' + Classes[0] + 'Stimuli' + '.png')
print normConfMatrix

normConfMatrix = normalizeMatrix(averageConfMatrix_visual)
#normConfMatrix = normalize(averageConfMatrix_visual, norm = 'l1', axis = 0)
plotMatrix(averageConfMatrix_visual, plotName = path + 'OutputT/Average_' + Classes[1] + 'Stimuli' + '.png')
print normConfMatrix

normConfMatrix = normalizeMatrix(averageConfMatrix_AV_C)
#normConfMatrix = normalize(averageConfMatrix_AV_C, norm = 'l1', axis = 0)
plotMatrix(averageConfMatrix_AV_C, plotName = path + 'OutputT/Average_' + Classes[2] + 'Stimuli' + '.png')
print normConfMatrix

normConfMatrix = normalizeMatrix(averageConfMatrix_AV_NC_A)
#normConfMatrix = normalize(averageConfMatrix_AV_NC_A, norm = 'l1', axis = 0)
plotMatrix(averageConfMatrix_AV_NC_A, plotName = path + 'OutputT/Average_' + Classes[3] + 'Stimuli' + '.png')
print normConfMatrix

normConfMatrix = normalizeMatrix(averageConfMatrix_AV_NC_V)
#normConfMatrix = normalize(averageConfMatrix_AV_NC_V, norm = 'l1', axis = 0)
plotMatrix(averageConfMatrix_AV_NC_V, plotName = path + 'OutputT/Average_' + Classes[4] + 'Stimuli' + '.png')
print normConfMatrix


