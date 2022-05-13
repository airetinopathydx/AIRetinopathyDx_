#This script takes the wavelet transform data
#from each animal and proceeds to labeling, balancing and filtering.
import re
import sys
import time
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join, splitext

#Read the files located in the script directory
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]
filesToRead = []

balanceList = ['ch1stziii2c_1', 'ch1stziii2a_1', 'ch1stziii1c_1', 'ch1stziii1b_1', 'ch1stziii1a_1', 'ch1stzii2b_1', 'ch1stzii2a_1', 'ch1stzii1b_1', 'ch1stzii1a_1', 'ch1stzi3b_1',
'ch1stzi3a_1', 'ch1stzi2c_1', 'ch1stzi2b_1', 'ch1stzi2a_1', 'ch1stzi1a_1', 'ch2stzi2b_1', 'ch2stzi2a_1', 'ch2stzi1a_1', 'ch1stziv1a_1', 'ch1stziii3c_1',
'ch1stziii3b_1', 'ch1stziii3a_1', 'ch2stziii3b_1', 'ch2stziii3a_1', 'ch2stziii2c_1', 'ch2stziii2a_1', 'ch2stziii1c_1', 'ch2stziii1b_1', 'ch2stziii1a_1',
'ch2stzii4d_1', 'ch2stzii4c_1', 'ch2stzii4b_1', 'ch2stzii4a_1', 'ch2stzii3c_1', 'ch2stzii3b_1', 'ch2stzii3a_1', 'ch2stzii2c_1', 'ch2stzii2b_1', 'ch2stzii2a_1',
'ch2stzii1b_1', 'ch2stzii1a_1', 'ch2stzi4c_1', 'ch2stzi4b_1', 'ch2stzi4a_1', 'ch2stzi3c_1', 'ch2stzi3b_1', 'ch2stzi3a_1', 'ch2stzi2c_1', 'ch2stziv5c_1',
'ch2stziv5b_1', 'ch2stziv5a_1', 'ch2stziv4c_1', 'ch2stziv4b_1', 'ch2stziv4a_1', 'ch2stziv3c_1', 'ch2stziv3b_1', 'ch2stziv3a_1', 'ch2stziv2b_1', 'ch2stziv2a_1',
'ch2stziv1d_1', 'ch2stziv1c_1', 'ch2stziv1b_1', 'ch2stziv1a_1', 'ch2stziii3c_1']


for f in arrFiles:
	fileName = splitext(f)[0]
	fileExtension = splitext(f)[1]
	#Avoid python files
	if ".py" not in fileExtension: 
		filesToRead.append(f)

mainDataFrame = pd.DataFrame()

#Start reading the preprocessed files for tagging and/or balancing
for f in filesToRead:
	fileName = splitext(f)[0]
	fileExtension = splitext(f)[1]
	if(mainDataFrame.empty == None):
		#Read csv file
		mainDataFrame = pd.read_csv(fileName + ".csv")
		#Gets the file size
		print("File size:" + str(len(mainDataFrame.index)))
	else:
		#Read csv file
		df = pd.read_csv(fileName + ".csv")
		#Gets the file size
		print("File size:" + str(len(df.index)))
		mainDataFrame = pd.concat([mainDataFrame, df], axis=0)

def getHealthStatus(patientNum, dic):
	return dic[patientNum]

def updateHealthStatus(df):
	#return df[['health.status']].applymap(lambda x: primeraCategorizacion[df['patient.number']])
	#df["health.status"] = [getHealthStatus(x, dic) for x in df['patient.number']]
	
	healthStatusList = []
	
	for index, row in df.iterrows():
		#print(row['c1'], row['c2'])
		
		fileName = row['patient']
		fileNameExtractFinal = "unknown"
		res = re.search('[a-z]{4,6}[0-9]+', fileName) #[a-z]{4,6}[0-9]+"),"[a-z]{4,6}")]
		if res is not None:
			fileNameExtract1 = str(res.group(0))
			print("fileNameExtract1:" + fileNameExtract1)
			res2 = re.search('[a-z]{4,6}', fileNameExtract1)

			if res2 is not None:
				fileNameExtractFinal = str(res2.group(0))
				print("fileNameExtractFinal:" + fileNameExtractFinal)
	
		if "stzi" == fileNameExtractFinal or "ctli" == fileNameExtractFinal:
			fileNameExtractFinal = "week4"
		
		if "stzii" == fileNameExtractFinal or "ctlii" == fileNameExtractFinal:
			fileNameExtractFinal = "week6"
			
		if "stziii" == fileNameExtractFinal or "ctliii" == fileNameExtractFinal:
			fileNameExtractFinal = "week8"
			
		if "stziv" == fileNameExtractFinal or "ctliv" == fileNameExtractFinal:
			fileNameExtractFinal = "week12"
			
		#print("fileNameExtractFinal:" + fileNameExtractFinal)
		healthStatusList.append(fileNameExtractFinal)
	
	df['health.status'] = healthStatusList
	
	return df
	
def balanceData(df,dic,balanceList):
	patients = dic.keys()
	print(patients)
	removePatients = [x for x in patients if x not in balanceList]
	print(removePatients)
	for patientNumber in removePatients:
		df = df[~df['patient.number'].isin(removePatients)]
	return df
	
def balanceByListPatientFileNames(df, listPython):
	removePatientsFileNames = []
	#Iter from the dataframe
	for index, row in df.iterrows():
		#If the patient filename is not in list.
		if ( row['patient'] not in listPython ):
			#Create a new slot for the patient filename to remove
			if row['patient'] not in removePatientsFileNames:
				#Consider to remove the patient filename from the dataframe
				removePatientsFileNames.append(row['patient'])
	print(removePatientsFileNames)
	#Iter to remove all the excluded patients filenames
	for patientFName in removePatientsFileNames:
			df = df.loc[~(df['patient'] == patientFName),:]
	return df
	
def getObs(fileName):
	reNum = re.search(r'_\d+$', fileName)
	return reNum.group(0)[1:]
	
def updateObs(df):
	df["obs"] = [getObs(x) for x in df['patient']]
	#Remove patient.number column
	df = df.drop(columns=['patient.number'])
	return df
	
def signalFilter01_40Hz(df):
	colRemove = []
	for i in range(1,22): #[f_000001 - f_000021] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	for i in range(109,145): #[f_000109 - f_000144] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	df = df.drop(colRemove, axis=1)
	colRename = {}
	for i in range(22,109): #Rename to [f_000001 - f_000087]
		colName = "f_"
		colName +='{:06d}'.format(i)
		newcolName = "f_"
		newcolName += '{:06d}'.format(i-21)
		colRename[colName] = newcolName 
	df = df.rename(columns = colRename)
	return df
	
def signalFilter09_2_1Hz(df):
	colRemove = []
	for i in range(1,54): #[f_000001 - f_000053] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	for i in range(67,145): #[f_000067 - f_000144] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	df = df.drop(colRemove, axis=1)
	colRename = {}
	for i in range(54,67): #Rename to [f_000001 - f_000013]
		colName = "f_"
		colName +='{:06d}'.format(i)
		newcolName = "f_"
		newcolName += '{:06d}'.format(i-53)
		colRename[colName] = newcolName 
	df = df.rename(columns = colRename)
	return df
	
def STZMiceEvo_01_40Hz(mainDataFrame):
	#Updates the labels of the health status.
	mainDataFrame = updateHealthStatus(mainDataFrame)

	#Balance/filter data set (if necessary)
	mainDataFrame = balanceByListPatientFileNames(mainDataFrame, balanceList)

	#Filters the preprocessed wavelet signal to the required frequency range
	mainDataFrame = signalFilter01_40Hz(mainDataFrame)
	print(mainDataFrame)

	#Save the dataframe in csv format
	mainDataFrame.to_csv("save\dfGrupo STZ mice evolution CH1y2_0.1_40HzBalanceo_G.csv", index=False, header=True)
	
def STZMiceEvo_09_2_1Hz(mainDataFrame):
	#Updates the labels of the health status.
	mainDataFrame = updateHealthStatus(mainDataFrame)

	#Balance/filter data set (if necessary)
	mainDataFrame = balanceByListPatientFileNames(mainDataFrame, balanceList)

	#Filters the preprocessed wavelet signal to the required frequency range
	mainDataFrame = signalFilter09_2_1Hz(mainDataFrame)
	print(mainDataFrame)

	#Save the dataframe in csv format
	mainDataFrame.to_csv("save\dfGrupo STZ mice evolution CH1y2_0.9_2.1HzBalanceo_G.csv", index=False, header=True)
	

### Main Program ###

#Update the column with the observation number.
mainDataFrame = updateObs(mainDataFrame)

## Generate dataframes ##
	
STZMiceEvo_01_40Hz(mainDataFrame)
STZMiceEvo_09_2_1Hz(mainDataFrame)