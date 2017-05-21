from os import listdir
import csv
import numpy as np


def subjectsAverage(path, flag):
	if flag == 1: all_results = np.zeros(5)
	else: all_results = np.zeros((3,5))

	listOfResults = listdir(path)

	for result in listOfResults:
		print result
		data_temp = []
		with open(path + result) as f:
			reader = csv.reader(f)
			for line in reader: data_temp.append(line)
		print all_results
		print np.array(data_temp, dtype=np.float32)
		all_results = all_results + np.array(data_temp, dtype=np.float32)

	averageResult = all_results/7
	return averageResult


path  = 'C:/Users/natad/Documents/SMC/MasterThesis/DataPostprocessing/Classification/'

# Compute average
newpath = path + 'Results/'
listOfResultFolders = listdir(newpath)
flag = 0

for folder in listOfResultFolders:
	print folder
	if folder == 'Response_vs_Expected': flag = 1
	print flag
	averageResult = subjectsAverage(newpath + folder+ '/', flag)
	print averageResult