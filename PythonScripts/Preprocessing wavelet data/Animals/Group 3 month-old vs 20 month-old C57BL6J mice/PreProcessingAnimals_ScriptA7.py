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

balanceList = ['controlc573months4oiesco_3', 'controlc573months4oiesco_2', 'controlc573months4oiesco_1', 'controlc573months2odesco_5', 'controlc573months2odesco_4',
'controlc573months2odesco_3', 'controlc573months2odesco_2', 'controlc573months2odesco_1', 'controlc573months5oiesco_5', 'controlc573months5oiesco_4',
'controlc573months5oiesco_3', 'controlc573months5oiesco_2', 'envejecidosc5720months_2lignedebase0-500hz1_3', 'envejecidosc5720months_2lignedebase0-500hz1_2',
'envejecidosc5720months_2lignedebase0-500hz1_1', 'envejecidosc5720months_1lignedebase0-500hz1_4', 'envejecidosc5720months_1lignedebase0-500hz1_3',
'envejecidosc5720months_1lignedebase0-500hz1_2', 'envejecidosc5720months_1lignedebase0-500hz1_1', 'envejecidosc5720months_3lignedebase0-500hz1_4',
'envejecidosc5720months_3lignedebase0-500hz1_3', 'envejecidosc5720months_3lignedebase0-500hz1_2', 'envejecidosc5720months_3lignedebase0-500hz1_1',
'envejecidosc5720months_2lignedebase0-500hz1_4']


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


def G3monthvs20month_01_40Hz(mainDataFrame):
	#Updates the labels of the health status.
	mainDataFrame = updateHealthStatus(mainDataFrame)

	#Balance/filter data set (if necessary)
	mainDataFrame = balanceByListPatientFileNames(mainDataFrame, balanceList)

	#Filters the preprocessed wavelet signal to the required frequency range
	mainDataFrame = signalFilter01_40Hz(mainDataFrame)
	print(mainDataFrame)

	#Save the dataframe in csv format
	mainDataFrame.to_csv("save\dfGrupo 3 month-old vs 20 month-old C57BL6J mice_0.1_40HzBalanceo_G.csv", index=False, header=True)
	
def G3monthvs20month_09_2_1Hz(mainDataFrame):
	#Updates the labels of the health status.
	mainDataFrame = updateHealthStatus(mainDataFrame)

	#Balance/filter data set (if necessary)
	mainDataFrame = balanceByListPatientFileNames(mainDataFrame, balanceList)

	#Filters the preprocessed wavelet signal to the required frequency range
	mainDataFrame = signalFilter09_2_1Hz(mainDataFrame)
	print(mainDataFrame)

	#Save the dataframe in csv format
	mainDataFrame.to_csv("save\dfGrupo 3 month-old vs 20 month-old C57BL6J mice_0.9_2.1HzBalanceo_G.csv", index=False, header=True)
	

### Main Program ###

#Update the column with the observation number.
mainDataFrame = updateObs(mainDataFrame)

## Generate dataframes ##
	
G3monthvs20month_01_40Hz(mainDataFrame)
G3monthvs20month_09_2_1Hz(mainDataFrame)