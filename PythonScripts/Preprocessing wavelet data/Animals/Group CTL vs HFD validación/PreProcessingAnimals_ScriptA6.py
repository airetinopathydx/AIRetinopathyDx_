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

balanceList = ['ctlvi1od(1)_2', 'ctlvi1od(1)_1', 'ctlv3oi_2', 'ctlv3oi_1', 'ctlv3oi(1)_2', 'ctlv3oi(1)_1', 'ctlv3od_2', 'ctlv3od_1', 'ctlv3od(1)_2', 'ctlv3od(1)_1', 'ctlv2oi_2',
'ctlv2oi_1', 'ctlv2oi(1)_2', 'ctlv2oi(1)_1', 'ctlv2od_2', 'ctlv2od_1', 'ctlv2od(1)_2', 'ctlv2od(1)_1', 'ctlv1oi_2', 'ctlv1oi_1', 'ctlv1oi(1)_2', 'ctlv1oi(1)_1',
'ctlv1od_2', 'ctlv1od_1', 'ctlv1od(1)_2', 'ctlv1od(1)_1', 'ctliv3oi_2', 'ctliv3oi_1', 'ctliv3od_2', 'ctliv3od_1', 'ctliv2oi_2', 'ctliv2oi_1', 'ctliv2od_2',
'ctliv2od_1', 'ctliv1oi_2', 'ctliv1oi_1', 'ctliv1oi(1)_2', 'ctliv1oi(1)_1', 'ctliv1od_2', 'ctliv1od_1', 'ctliv1od(1)_2', 'ctliv1od(1)_1', 'hfdiv1oi(1)_2',
'hfdiv1oi(1)_1', 'hfdiv1od_2', 'hfdiv1od_1', 'hfdiv1od(1)_2', 'hfdiv1od(1)_1', 'ctlxii3oi_2', 'ctlxii3oi_1', 'ctlxii3oi(1)_2', 'ctlxii3oi(1)_1', 'ctlxii3od_2',
'ctlxii3od_1', 'ctlxii3od(1)_2', 'ctlxii3od(1)_1', 'ctlxii2oi_2', 'ctlxii2oi_1', 'ctlxii2oi(1)_2', 'ctlxii2oi(1)_1', 'ctlxii2od_2', 'ctlxii2od_1', 'ctlxii2od(1)_2',
'ctlxii2od(1)_1', 'ctlxii1oi_2', 'ctlxii1oi_1', 'ctlxii1oi(1)_2', 'ctlxii1oi(1)_1', 'ctlxii1od_2', 'ctlxii1od_1', 'ctlvi2oi_2', 'ctlvi2oi_1', 'ctlvi2oi(1)_2',
'ctlvi2oi(1)_1', 'ctlvi2od_2', 'ctlvi2od_1', 'ctlvi2od(1)_2', 'ctlvi2od(1)_1', 'ctlvi1oi_2', 'ctlvi1oi_1', 'ctlvi1oi(1)_2', 'ctlvi1oi(1)_1', 'ctlvi1od_2',
'ctlvi1od_1', 'hfdvi1od(1)_1', 'hfdv3oi_2', 'hfdv3oi_1', 'hfdv3oi(1)_2', 'hfdv3oi(1)_1', 'hfdv3od_2', 'hfdv3od_1', 'hfdv3od(1)_2', 'hfdv3od(1)_1', 'hfdv2oi_2',
'hfdv2oi_1', 'hfdv2oi(1)_2', 'hfdv2oi(1)_1', 'hfdv2od_2', 'hfdv2od_1', 'hfdv2od(1)_2', 'hfdv2od(1)_1', 'hfdv1oi_2', 'hfdv1oi_1', 'hfdv1oi(1)_2', 'hfdv1oi(1)_1',
'hfdv1od_2', 'hfdv1od_1', 'hfdv1od(1)_2', 'hfdv1od(1)_1', 'hfdiv3oi_2', 'hfdiv3oi_1', 'hfdiv3oi(1)_2', 'hfdiv3oi(1)_1', 'hfdiv3od_2', 'hfdiv3od_1', 'hfdiv3od(1)_2',
'hfdiv3od(1)_1', 'hfdiv2oi_2', 'hfdiv2oi_1', 'hfdiv2oi(1)_2', 'hfdiv2oi(1)_1', 'hfdiv2od_2', 'hfdiv2od_1', 'hfdiv2od(1)_2', 'hfdiv2od(1)_1', 'hfdiv1oi_2',
'hfdiv1oi_1', 'hfdxii3oi_2', 'hfdxii3oi_1', 'hfdxii3oi(1)_2', 'hfdxii3oi(1)_1', 'hfdxii3od_2', 'hfdxii3od_1', 'hfdxii2oi_2', 'hfdxii2oi_1', 'hfdxii2oi(1)_2',
'hfdxii2oi(1)_1', 'hfdxii2od_2', 'hfdxii2od_1', 'hfdxii2od(1)_2', 'hfdxii2od(1)_1', 'hfdxii1oi_2', 'hfdxii1oi_1', 'hfdxii1oi(1)_2', 'hfdxii1oi(1)_1',
'hfdxii1od_2', 'hfdxii1od_1', 'hfdxii1od(1)_2', 'hfdxii1od(1)_1', 'hfdvi3oi_2', 'hfdvi3oi_1', 'hfdvi3od_2', 'hfdvi3od_1', 'hfdvi2oi_2', 'hfdvi2oi_1', 'hfdvi2oi(1)_2']


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
		res = re.search('[a-z]{3,4}', fileName) #"[a-z]{3,4}"),"[a-z]{3,4}")]
		if res is not None:
			fileNameExtract1 = str(res.group(0))
			#print("fileNameExtract1:" + fileNameExtract1)
			res2 = re.search('[a-z]{3,4}', fileNameExtract1)

			if res2 is not None:
				fileNameExtractFinal = str(res2.group(0))
				#print("fileNameExtractFinal:" + fileNameExtractFinal)
	
		if "stzi" in fileNameExtractFinal or "jstz" in fileNameExtractFinal or "rpp" in fileNameExtractFinal or "enve" in fileNameExtractFinal or "obb" in fileNameExtractFinal or "hfdx" in fileNameExtractFinal or "hfdi" in fileNameExtractFinal or "hfdv" in fileNameExtractFinal:
			fileNameExtractFinal = "disorder"
		
		if "ctrl" in fileNameExtractFinal or "jctr" in fileNameExtractFinal or "ctlv" in fileNameExtractFinal or "ctlx" in fileNameExtractFinal or "ctli" in fileNameExtractFinal or "cont" in fileNameExtractFinal or "lean" in fileNameExtractFinal:
			fileNameExtractFinal = "health"
			
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

	
def CTLvsHFD_01_40Hz(mainDataFrame):
	#Updates the labels of the health status.
	mainDataFrame = updateHealthStatus(mainDataFrame)

	#Balance/filter data set (if necessary)
	mainDataFrame = balanceByListPatientFileNames(mainDataFrame, balanceList)

	#Filters the preprocessed wavelet signal to the required frequency range
	mainDataFrame = signalFilter01_40Hz(mainDataFrame)
	print(mainDataFrame)

	#Save the dataframe in csv format
	mainDataFrame.to_csv("save\dfGrupo CTL vs HFD validación_0.1_40HzBalanceo_G.csv", index=False, header=True)
	
def CTLvsHFD_09_2_1Hz(mainDataFrame):
	#Updates the labels of the health status.
	mainDataFrame = updateHealthStatus(mainDataFrame)

	#Balance/filter data set (if necessary)
	mainDataFrame = balanceByListPatientFileNames(mainDataFrame, balanceList)

	#Filters the preprocessed wavelet signal to the required frequency range
	mainDataFrame = signalFilter09_2_1Hz(mainDataFrame)
	print(mainDataFrame)

	#Save the dataframe in csv format
	mainDataFrame.to_csv("save\dfGrupo CTL vs HFD validación_0.9_2.1HzBalanceo_G.csv", index=False, header=True)
	

### Main Program ###

#Update the column with the observation number.
mainDataFrame = updateObs(mainDataFrame)

## Generate dataframes ##
	
CTLvsHFD_01_40Hz(mainDataFrame)
CTLvsHFD_09_2_1Hz(mainDataFrame)