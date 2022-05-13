#This script takes the wavelet transform data from each validation patient
#and proceeds to labeling, balancing and filtering.
import re
import sys
import time
import random
import pandas as pd
import numpy as np
from os import listdir
from joblib import Parallel, delayed
from os.path import isfile, join, splitext

#Reads the files located in the script directory.
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]
filesToRead = []

for f in arrFiles:
	fileName = splitext(f)[0]
	fileExtension = splitext(f)[1]
	#Avoid python files.
	if ".py" not in fileExtension:
		filesToRead.append(f)

mainDataFrame = pd.DataFrame()

#External validation set labels.
secondLabelingExtVal = {112:'disorder',114:'health',
116:'health',117:'health',120:'disorder',122:'health',
124:'health',126:'health',127:'disorder',130:'disorder',
132:'health',134:'disorder',136:'health',138:'disorder',
140:'health',142:'disorder',144:'health',146:'health',
148:'disorder',150:'health',152:'health',154:'disorder',
156:'disorder',158:'disorder',160:'disorder',
162:'health',164:'disorder',166:'disorder',168:'disorder',
170:'disorder',172:'disorder',174:'disorder',176:'disorder',
178:'disorder',180:'disorder',182:'disorder',184:'disorder',
186:'disorder',188:'disorder',190:'disorder',192:'disorder',
194:'disorder',196:'disorder',198:'disorder',200:'health',
202:'disorder',204:'disorder',206:'disorder',208:'disorder',
210:'disorder',212:'disorder',214:'disorder',216:'disorder',
218:'disorder',220:'disorder',222:'disorder',224:'disorder',
226:'disorder',228:'disorder',230:'disorder',234:'disorder',
236:'health',238:'disorder',240:'disorder',242:'disorder',
244:'health',246:'health',248:'health',250:'disorder',
252:'disorder',254:'health',256:'disorder',258:'disorder',
260:'disorder',262:'disorder',264:'disorder',266:'disorder',
268:'disorder',270:'disorder',272:'disorder',274:'disorder',
276:'disorder',278:'disorder',280:'disorder',282:'health',
284:'health',286:'disorder',288:'disorder',290:'disorder',
292:'disorder',294:'disorder',296:'disorder',298:'health',
300:'disorder',302:'disorder',304:'disorder',306:'disorder',
308:'disorder',310:'disorder',312:'disorder',314:'disorder',
316:'disorder',318:'disorder',320:'health',322:'disorder',
324:'disorder',326:'disorder',328:'disorder',330:'disorder',
332:'disorder',334:'disorder',336:'health',338:'disorder',
340:'disorder',342:'disorder',344:'disorder',346:'disorder',
348:'disorder',350:'disorder',352:'disorder',354:'disorder',
356:'disorder',358:'disorder',360:'disorder',362:'disorder',
364:'disorder',366:'disorder',368:'health',370:'health',
372:'disorder',374:'disorder',376:'disorder',378:'disorder',
380:'disorder',382:'disorder',384:'disorder',386:'disorder',
388:'disorder',390:'disorder',392:'disorder', 394:'disorder',
396:'health',398:'health',400:'disorder',402:'disorder',
404:'health',406:'health',408:'disorder',410:'disorder',
412:'health',414:'disorder',416:'disorder',418:'disorder',
420:'disorder',422:'health',424:'health',426:'disorder',
428:'disorder',
430:'disorder',432:'health',434:'disorder',436:'disorder',
438:'disorder',440:'disorder',442:'disorder',444:'disorder',
446:'disorder',448:'disorder',450:'disorder',452:'disorder',
454:'health',456:'health',458:'health',460:'health',
462:'health',464:'health',466:'disorder',468:'disorder',
470:'disorder',472:'health',474:'disorder',476:'disorder'
}

#Start reading the preprocessed files for labeling and/or balancing
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

def updateHealthStatus(df, dic):
	#return df[['health.status']].applymap(lambda x: primeraCategorizacion[df['patient.number']])
	df["health.status"] = [getHealthStatus(x, dic) for x in df['patient.number']]
	return df
	
def getObs(fileName):
	reNum = re.search(r'_\d+$', fileName)
	return reNum.group(0)[1:]
	
def updateObs(df):
	df["obs"] = [getObs(x) for x in df['patient']]
	return df
	
def cleanDataEx(df):
	df = df.drop(df.columns[0], axis=1)
	df["obs"] = pd.to_numeric(df["obs"])
	df["patient.number"] = pd.to_numeric(df["patient.number"])
	df = df.loc[~((df['patient.number'] < 68) & (df['obs'] > 5)),:] #2nd labeling
	#df = df.loc[~((df['health.status'] == 'disorder') & (df['obs'] > 3)),:] #Balancing 1st labeling
	return df
	
#Function that filters the wavelet signal of each patient.
def signalFilter0_3_40Hz(df):
	colRemove = []
	for i in range(1,38): #[f_000001 - f_000037] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	for i in range(109,145): #[f_000109 - f_000144] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	df = df.drop(colRemove, axis=1)
	#Rename the columns
	colRename = {}
	for i in range(38,109): #Rename to [f_000001 - f_000071]
		colName = "f_"
		colName +='{:06d}'.format(i)
		newcolName = "f_"
		newcolName += '{:06d}'.format(i-37)
		colRename[colName] = newcolName 
	df = df.rename(columns = colRename)
	return df

####
#Functions to balance automaticaly (random)
###

def findToRemoveClass(df, className):
	tmpdf = df.loc[~((df['health.status'] != className)),:]
	randomNumber = random.randint(0, tmpdf.shape[0])
	print("Size: ", tmpdf.shape[0])
	randomPatientData = tmpdf.iloc[randomNumber]
	print(randomPatientData)
	return (randomPatientData['patient.number'], randomPatientData['obs'])

def countClasses(df):
	classesCount = df.pivot_table(columns=['health.status'], aggfunc='size')
	print("---------")
	print(list(classesCount.keys()))
	print(classesCount)
	print("---------")
	return (list(classesCount.keys()), classesCount)

def areEqualClasses(classesNames, classesCount):
	equal = -1
	for classesName in classesNames:
		if (equal == -1):
			equal = int(classesCount[classesName])
		else:
			if(int(classesCount[classesName]) != equal):
				return False
	return True

def getHighestClass(classesNames, classesCount):
	highest = -1
	highestClass = ""
	for classesName in classesNames:
		if highest < int(classesCount[classesName]):
			highest = int(classesCount[classesName])
			highestClass = str(classesName)
	return (highestClass, highest)

#This function auto balance the classes (control/disorder) randomly.
def autoBalanceClasses(df):
	(classesNames, classesCount) = countClasses(df)
	while(areEqualClasses(classesNames, classesCount) == False and classesCount[0] > 0):
		(classToRemove, _) = getHighestClass(classesNames, classesCount)
		(patientNumber, obsNumber) = findToRemoveClass(df, classToRemove)
		#Remove a patient randomly to balance the data of the highest class
		df = df.loc[~((df['patient.number'] == patientNumber) & (df['obs'] == obsNumber)),:]
		(classesNames, classesCount) = countClasses(df)
	return df
		

### Main program ###

#Update the column with the observation number of each patient.
mainDataFrame = updateObs(mainDataFrame)

#Updates the health labels according to the indicated dictionary.
mainDataFrame = updateHealthStatus(mainDataFrame, secondLabelingExtVal)
print(mainDataFrame)

#Deletes records with patient number < 68 and number of obs > 5, because of repetition of the signal.
mainDataFrame = cleanDataEx(mainDataFrame)
print(mainDataFrame)

#Filter the defined range of values of the signal.
mainDataFrame = signalFilter0_3_40Hz(mainDataFrame)
print(mainDataFrame)

#Auto balance the dataset randomly
mainDataFrame = autoBalanceClasses(mainDataFrame)
print(mainDataFrame)

#Save the dataframe in csv format.
mainDataFrame.to_csv("save\dfValidacionExternaEtiquetado_0.3_40Hz_Balanceado.csv", index=False, header=True)