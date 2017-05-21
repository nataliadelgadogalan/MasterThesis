import sys
sys.path.append("C:/Python27")
from os import listdir
import csv
import numpy as np
from scipy.stats.stats import pearsonr
from itertools import islice
import seaborn as sns;
import matplotlib.pyplot as plt
from minepy import MINE

path = 'C:/Users/natad/Documents/SMC/MasterThesis/DataPostprocessing/Correlation/'

### FUNCTIONS ###

def readfile(filename, flag):
	data_temp = []
	with open(filename) as f:
		reader = csv.reader(f)
		for line in reader: 
			if flag == 0: 
				data_temp.append(line)
			else: 
				data_temp.append(line[:-2])

	names = data_temp[0]
	attributes = np.array(data_temp[1:], dtype=np.float32)

	return names, attributes

def normalization(X):
	sizeX = X.shape
	for i in range (0, sizeX[1]):
		maxX = max(X[:,i])
		minX = min(X[:,i])
		X[:,i] = (X[:,i] - minX) / (maxX -minX)
	return X

def correlation(X,Y, sizeX, sizeY):
	RangeFor = min(sizeX[0], sizeY[0])
	PearsonCorrMatrix = np.zeros((2,sizeX[1],sizeY[1]))
	MINECorrMatrix = np.zeros((sizeX[1],sizeY[1]))
	for a in range (0,sizeX[1]):
		for b in range (0,sizeY[1]):
			mine = MINE(alpha=0.6, c=15)
			mine.compute_score(X[:,a],Y[:,b])
			MINECorrMatrix[a,b]=mine.mic()
			r, p = pearsonr(X[:,a],Y[:,b])
			PearsonCorrMatrix[0,a,b]=r
			PearsonCorrMatrix[1,a,b]=p
	
	return PearsonCorrMatrix, MINECorrMatrix

def rankCorrelation (correlationMatrix, type):
	N = 5
	sizeC = correlationMatrix.shape
	maxValues = []
	indexMaxValues = []
	if type == 0: 
		for i in range (0, int(sizeC[0])):
			correlationMatrix[i,i] = 0
	correlationMatrix = np.array(correlationMatrix)
	for j in range (0, N):
		maxValue = np.amax(correlationMatrix)
		index = np.where(correlationMatrix == maxValue)
		aux_index = [int(index[0][0]), int(index[1][0])]
		# we keep the first max, and delete it from the correlation matrix to find the next max
		correlationMatrix[aux_index] = 0
		maxValues.append(maxValue)

		indexMaxValues.append(aux_index)

	return maxValues, indexMaxValues
	

def printRank(maxValues, indexMaxValues, Vocab1, Vocab2):
	for i in range (0, int(len(maxValues))):
		idx = indexMaxValues[i]
		format_list = [i+1, Vocab1[idx[0]], Vocab2[idx[1]], maxValues[i]]
		print "{}. {} is most correlated with {} with a {} correlation".format(*format_list)

	

def plotCorrelations (cMatrix, x_label, y_label, plotName):
	ax = sns.heatmap(cMatrix, vmin = 0, vmax = 1)
	ax.set_ylabel(y_label)
	ax.set_xlabel(x_label)
	sns.plt.show()
	fig = ax.get_figure()
	fig.savefig(plotName)



########## START CODE ###################

# Read files
newpath = path + 'Data/'
listOfSubjects = listdir(newpath)

for subject in listOfSubjects:

	# READ FILES OF FEATURES
	listOfFiles = listdir(newpath + subject + '/')
	audioFeatureNames, audioFeatures = readfile(newpath + subject + '/' + listOfFiles[0], flag = 0)
	EEGFeatureNames, EEGFeatures = readfile(newpath + subject + '/' + listOfFiles[1], flag = 1)


	### EXTRACT SIZE OF DATA ###
	sizeAF = audioFeatures.shape
	sizeEF = EEGFeatures.shape

	### NORMALIZATION OF DATASET ###
	AF_norm = normalization(audioFeatures)
	EF_norm = normalization(EEGFeatures)


	### CORRELATIONS EXTRACTION ###
	PcorrMatrixG1G1, McorrMatrixG1G1=correlation(X=AF_norm,Y=EF_norm, sizeX=sizeAF, sizeY=sizeEF)
	abs_corrMatrix = abs(PcorrMatrixG1G1)

	### CORRELATIONS RANKING ###
	print 'Maximum correlations between audio features and EEG features for pearson correlation:'
	maxValues, indexMaxValues = rankCorrelation (abs_corrMatrix[0][1:,1:], type = 1)
	printRank(maxValues = maxValues, indexMaxValues = indexMaxValues, Vocab1 = audioFeatureNames, Vocab2 = EEGFeatureNames)

	### HEATMAPS ###
	plotCorrelations (cMatrix = abs_corrMatrix[0][1:,1:], x_label = 'Audio features', y_label = 'EEG features', plotName = newpath + subject + '/Correlation_Matrix.png')
