#This script takes the wavelet transform data
#from each patient and proceeds to labeling, balancing and filtering.
import re
import sys
import time
import pandas as pd
import numpy as np
from os import listdir
from joblib import Parallel, delayed
from os.path import isfile, join, splitext

#Import dictionaries to balance the data
import BalanceData as bd

#Reads the files located in the script directory
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]
filesToRead = []

for f in arrFiles:
	fileName = splitext(f)[0]
	fileExtension = splitext(f)[1]
	#Avoid python files
	if ".py" not in fileExtension: 
		filesToRead.append(f)

mainDataFrame = pd.DataFrame()

#Labels assigned to each patient (Second categorization)
secondLabeling = {1:'disorder',2:'disorder',3:'disorder',
4:'health',5:'disorder',6:'disorder',7:'disorder',
8:'disorder',9:'disorder',10:'disorder',11:'disorder',
12:'disorder',13:'health',14:'disorder',15:'disorder',
16:'disorder',17:'disorder',18:'disorder',19:'disorder',
20:'disorder',21:'disorder',22:'disorder',23:'disorder',
24:'disorder',25:'disorder',26:'disorder',27:'disorder',
28:'disorder',29:'disorder',30:'disorder',31:'disorder',
32:'disorder',33:'disorder',34:'disorder',35:'health',
36:'disorder',37:'disorder',38:'health',39:'disorder',
40:'disorder',42:'health',43:'health',44:'health',
45:'health',46:'disorder',47:'health',48:'disorder',
49:'health',50:'disorder',51:'health',52:'disorder',
53:'health',54:'health',55:'disorder',56:'health',
57:'health',58:'health',59:'disorder',60:'health',
61:'health',63:'disorder',64:'disorder',68:'disorder',
69:'disorder',70:'disorder',71:'disorder',72:'health',
73:'health',74:'disorder',75:'disorder',76:'disorder',
77:'disorder',78:'disorder',79:'disorder',80:'disorder',
81:'disorder',82:'disorder',83:'disorder',84:'disorder',
85:'disorder',86:'disorder',87:'disorder',88:'disorder',
89:'disorder',90:'disorder',91:'disorder',92:'disorder',
93:'disorder',94:'disorder',95:'disorder',96:'disorder',
97:'disorder',98:'disorder',99:'disorder',100:'disorder',
101:'disorder',102:'disorder',103:'disorder',104:'health',
105:'health',106:'disorder',107:'disorder',108:'disorder',
109:'disorder',110:'health',111:'disorder',113:'health',
115:'health',118:'health',119:'disorder',121:'health',
123:'health',125:'health',128:'disorder',129:'disorder',
131:'health',133:'disorder',135:'health',137:'disorder',
139:'health',141:'disorder',143:'health',145:'health',
147:'disorder',149:'health',151:'health',153:'disorder',
155:'disorder',157:'disorder',159:'disorder',161:'health',
163:'disorder',165:'disorder',167:'disorder',169:'disorder',
171:'disorder',173:'disorder',175:'disorder',177:'disorder',
179:'disorder',181:'disorder',183:'disorder',185:'disorder',
187:'disorder',189:'disorder',191:'disorder',193:'disorder',
195:'disorder',197:'disorder',199:'health',201:'disorder',
203:'disorder',205:'disorder',207:'disorder',209:'disorder',
211:'disorder', 213:'disorder',215:'disorder',217:'disorder',
219:'disorder',221:'disorder',223:'disorder',225:'disorder',
227:'disorder',229:'disorder',231:'disorder',232:'disorder',
233:'disorder',235:'health',237:'disorder',239:'disorder',
241:'disorder',243:'health',245:'health',247:'health',
249:'disorder',251:'disorder',253:'health',255:'disorder',
257:'disorder',259:'disorder',261:'disorder',263:'disorder',
265:'disorder',267:'disorder',269:'disorder',271:'disorder',
273:'disorder',275:'disorder',277:'disorder',279:'disorder',
281:'health',283:'health',285:'disorder',287:'disorder',
289:'disorder',291:'disorder',293:'disorder',295:'disorder',
297:'health',299:'disorder',301:'disorder',303:'disorder',
305:'disorder',307:'disorder',309:'disorder',311:'disorder',
313:'disorder',315:'disorder',317:'disorder',319:'health',
321:'disorder',323:'disorder',325:'disorder',327:'disorder',
329:'disorder',331:'disorder',333:'disorder',335:'health',
337:'disorder',339:'disorder',341:'disorder',343:'disorder',
345:'disorder',347:'disorder',349:'disorder',351:'disorder',
353:'disorder',355:'disorder',357:'disorder',359:'disorder',
361:'disorder',363:'disorder',365:'disorder',367:'health',
369:'health',371:'disorder',373:'disorder',375:'disorder',
377:'disorder',379:'disorder',381:'disorder',383:'disorder',
385:'disorder',387:'disorder',389:'disorder',391:'disorder',
393:'disorder',395:'health',397:'health',399:'disorder',
401:'disorder',403:'health',405:'health',407:'disorder',
409:'disorder',411:'health',413:'disorder',415:'disorder',
417:'disorder',419:'disorder',421:'health',423:'health',
425:'disorder',427:'disorder',429:'disorder',431:'health',
433:'disorder',435:'disorder',437:'disorder',439:'disorder',
441:'disorder',443:'disorder',445:'disorder',447:'disorder',
449:'disorder',451:'disorder',453:'health',455:'health',
457:'health',459:'health',461:'health',463:'health',
465:'disorder',467:'disorder',469:'disorder',471:'health',
473:'disorder',475:'disorder',477:'disorder',478:'disorder',
479:'health',480:'health',481:'disorder',482:'disorder',
483:'disorder',484:'disorder',487:'disorder',488:'disorder',
489:'disorder',490:'disorder',491:'disorder',492:'disorder',
493:'disorder',494:'disorder',495:'disorder',496:'disorder',
497:'disorder',498:'disorder',499:'health',500:'health',
501:'disorder',
502:'disorder',503:'disorder',504:'disorder',505:'disorder',
506:'disorder',507:'disorder',508:'disorder',509:'disorder',
510:'disorder',511:'disorder',512:'disorder',513:'disorder',
514:'disorder',515:'disorder',516:'disorder',517:'disorder',
518:'disorder',519:'disorder',520:'disorder',529:'disorder',
530:'disorder',531:'disorder',532:'disorder',533:'disorder',
534:'disorder',535:'disorder'}

#Labels assigned to each patient (First categorization)
firstLabeling = {
1:"disorder",2:"disorder",3:"disorder",
4:"health",5:"disorder",6:"disorder",
7:"disorder",8:"disorder",9:"disorder",
10:"disorder",11:"disorder",12:"disorder",
13:"disorder",14:"disorder",15:"disorder",
16:"disorder",17:"disorder",18:"disorder",
19:"disorder",20:"disorder",21:"disorder",
22:"disorder",23:"disorder",24:"disorder",
25:"disorder",26:"disorder",27:"disorder",
28:"disorder",29:"disorder",30:"disorder",
31:"disorder",32:"disorder",33:"disorder",
34:"disorder",35:"health", 36:"enfermo",
37:"disorder",
38:"health",39:"disorder",40:"disorder",
42:"disorder",43:"disorder",44:"health",
45:"health",46:"health",47:"disorder",
48:"disorder",49:"health",50:"health",
51:"health",52:"health",53:"health",
54:"health",55:"disorder",56:"disorder",
57:"health",58:"health",59:"disorder",
60:"health",61:"disorder",62:"disorder",
63:"disorder",64:"disorder",68:"disorder",
69:"disorder",70:"disorder",71:"disorder",
72:"health",73:"health",74:"disorder",
75:"disorder",76:"health",77:"health",
78:"disorder",79:"disorder",80:"health",
81:"health",82:"disorder",83:"disorder",
84:"health",85:"health",86:"disorder",
87:"disorder",88:"disorder",89:"disorder",
90:"disorder",91:"disorder",92:"disorder",
93:"disorder",94:"disorder",95:"disorder",
96:"disorder",97:"disorder",98:"disorder",
99:"disorder",100:"disorder",101:"disorder",
102:"disorder",103:"disorder",104:"health",
105:"health",106:"disorder",107:"disorder",
108:"disorder",109:"disorder",110:"health",
111:"disorder",113:"health",115:"health",
118:"health",119:"health",121:"health",
123:"health",125:"health",128:"disorder",
129:"disorder",131:"health",133:"health",
135:"health",137:"disorder",139:"health",
141:"disorder",143:"health",145:"health",
147:"disorder",149:"health",151:"health",
153:"disorder",155:"health",157:"disorder",
159:"disorder",161:"health",163:"disorder",
165:"health",167:"disorder",169:"disorder",
171:"health",173:"disorder",175:"health",
177:"disorder",179:"disorder",181:"disorder",
183:"disorder",185:"disorder",187:"disorder",
189:"disorder",191:"disorder",193:"health",
195:"disorder",197:"health",199:"health",
201:"disorder",203:"disorder",205:"disorder",
207:"disorder",209:"disorder",211:"disorder",
213:"disorder",215:"disorder",217:"disorder",
219:"disorder",221:"disorder",223:"disorder",
225:"disorder",227:"disorder",229:"disorder",
231:"disorder",232:"disorder",233:"health",
235:"health",237:"disorder",239:"disorder",
241:"disorder",243:"health",245:"health",
247:"health",249:"disorder",251:"disorder",
253:"health",255:"disorder",257:"disorder",
259:"disorder",261:"health",263:"health",
265:"disorder",267:"disorder",269:"disorder",
271:"disorder",273:"disorder",275:"disorder",
277:"disorder",279:"disorder",281:"health",
283:"health",285:"disorder",287:"disorder",
289:"health",291:"disorder",293:"disorder",
295:"health",297:"disorder",299:"disorder",
301:"health",303:"health",305:"disorder",
307:"disorder",309:"disorder",311:"health",
313:"disorder",315:"disorder",317:"disorder",
319:"health",321:"disorder",323:"disorder",
325:"disorder",327:"disorder",329:"disorder",
331:"disorder",333:"disorder",335:"health",
337:"disorder",339:"disorder",341:"disorder",
343:"disorder",345:"disorder",347:"disorder",
349:"disorder",351:"disorder",353:"disorder",
355:"health",357:"disorder",359:"disorder",
361:"disorder",363:"health",365:"disorder",
367:"health",369:"health",371:"disorder",
373:"disorder",375:"health",377:"disorder",
379:"disorder",381:"disorder",383:"disorder",
385:"disorder",387:"disorder",389:"disorder",
391:"disorder",393:"health",395:"health",
397:"health",399:"disorder",401:"health",
403:"health",405:"health",407:"disorder",
409:"disorder",411:"health",413:"disorder",
415:"disorder",417:"disorder",419:"disorder",
421:"health",423:"health",425:"health",
427:"disorder",429:"disorder",431:"health",
433:"disorder",435:"disorder",437:"disorder",
439:"disorder",441:"disorder",443:"disorder",
445:"disorder",447:"disorder",449:"disorder",
451:"disorder",453:"health",455:"health",
457:"health",459:"health",461:"health",
463:"health",465:"disorder",467:"disorder",
469:"disorder",471:"health",473:"disorder",
475:"disorder", 477:"disorder", 478:"disorder",
479:"health",480:"health",481:"health",
482:"health",483:"health",484:"health",
485:"disorder",486:"disorder",487:"disorder",
488:"disorder",489:"disorder",490:"disorder",
491:"health",492:"health",493:"disorder",
494:"disorder",495:"disorder",496:"disorder",
497:"disorder",498:"disorder",499:"health",
500:"health",501:"disorder",502:"disorder",
503:"disorder",504:"disorder",505:"disorder",
506:"disorder",507:"disorder",508:"disorder",
509:"health",510:"health",511:"health",
512:"health",513:"disorder",514:"disorder",
515:"health",516:"health",517:"health",
518:"health",519:"disorder",520:"disorder",
529:"disorder",530:"disorder",531:"disorder",
532:"disorder",533:"disorder",534:"disorder",
535:"disorder"
}

#Patient Balancing

#2daCat - (Health / Sick)
secondLabelingBalance = [
4,13,35,38,42,43,44,45,47,49,51,53,54,56,57,58,
60,61,72,73,104,105,110,113,115,118,121,123,125,
131,135,139,143,145,149,161,199,235,243,245,247,
253,281,283,297,319,335,367,369,395,397,403,405,
411,421,423,431,453,455,457,459,461,463,471,479,
480,499,500,

1,2,3,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,
22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,39,40,
46,48,50,52,59,63,64,68,69,70,71,74,75,76,77,78,
79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,
96,97,98,99,100,101,102,103,106,107,108,109,111,
133,137,147,151,159,163,167,169,171,185,203,211,213,
215,219,223,225,227,301,317,323,333,351,373,
437,439,443,467,469
]

firstLabelingBalance = [
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
16,17,18,19,20,21,22,23,24,25,26,27,
28,29,30,31,32,33,35,36,38,39,
40,42,43,44,45,46,47,48,49,50,51,
53,54,56,57,58,59,60,61,62,63,64,
68,69,70,71,72,73,74,75,76,77,80,81,
82,83,84,85,86,87,88,89,90,91,92,93,
94,95,96,97,98,99,102,103,104,105,108,
109,111,113,115,118,119,121,123,125,128,129,
131,133,135,137,139,141,143,145,147,149,
151,153,155,157,159,161,163,165,167,169,
171,173,175,193,197,199,
209,211,213,215,217,219,221,223,225,
231,232,233,235,237,239,243,245,247,
253,261,
263,265,267,269,271,273,275,277,279,281,
283,289,295,301,303,305,307,309,311,313,
315,317,319,321,
325,327,329,331,333,335,337,339,341,
343,345,347,349,355,363,365,369,367,375,377,379,
393,395,397,399,401,403,405,407,409,411,
421,423,425,431,453,455,457,459,461,463,471
]

#By type of disease 1st Cat (1st labeling)

prediabetes1stCat = [1,13,32,33,39,42,43,47,48,56,61,68,69,173,297,371,385,417,485,486,487,488]

MetS1stCat = [2,14,26,29,36,40,62,70,71,74,75,129,137,141,147,153,157,179,181,183,191,201,203,237,
239,249,251,255,257,265,267,275,277,279,299,307,309,325,331,339,343,347,349,357,359,
361,379,383,389,391,407,415,419,493,494,507,508]

Control1stCat = [4,35,38,44,45,46,49,50,51,52,53,54,57,58,60,72,73,76,77,80,81,84,85,104,105,110,
113,115,118,119,121,123,125,131,133,135,139,143,145,149,151,155,161,165,171,175,193,
197,199,233,235,243,245,247,253,261,263,281,283,289,295,301,303,311,319,335,355,363,367,
369,375,393,395,397,401,403,405,411,421,423,425,431,453,455,457,459,461,463,471,479,
480,481,482,483,484,491,492,499,500,509,510,511,512,515,516,517,518]

DMnoDR1stCat = [3,11,12,16,19,28,37,55,59,63,78,79,82,83,86,87,88,89,90,91,102,
103,159,187,189,205,207,209,215,259,269,271,287,291,293,305,317,327,329,337,341,
345,353,377,381,387,399,409,413,427,429,433,441,467,489,490,495,496,501,502,503,
504,513,514]

#By type of disease 2nd Cat (2nd labeling)

Control2ndCat = [4,13,35,38,42,43,44,45,47,49,51,53,54,56,57,58,60,61,72,73,104,105,110,
113,115,118,121,123,125,131,135,139,143,145,149,161,199,235,243,245,247,253,281,283,
297,319,335,367,395,397,403,405,411,423,431,453,455,457,459,461,471,479,480,499,
500] #151 omitted due to change in label (removed from overweight) -> healthy (now healhty)

Obese2ndCat = [76, 77, 155, 171, 263, 301, 303, 363, 371, 375, 511, 512, 515, 516,
517, 518]

MetS2ndCat = [2, 14, 26, 29, 36, 40, 70, 71, 74, 75, 129, 137, 141, 147,
153, 157, 179, 181, 183, 191, 201, 203, 237, 239, 249, 251, 255, 257, 265, 267,
275, 277, 279, 299, 307, 309, 325, 331, 339, 343, 347, 349, 357, 359, 361, 379,
383, 389, 391, 407, 415, 419, 493, 494, 507, 508]

OW2ndCat = [1, 33, 39, 46, 48, 50, 52, 68, 69, 80, 81, 84, 85, 119, 133, 165,
173, 175, 193, 197, 233, 261, 289, 295, 311, 355, 385, 393, 401, 417, 425, 481, 482,
483, 484, 487, 488, 491, 492, 509, 510]

DMnoDR2ndCat = [3, 11, 12, 16, 19, 28, 32, 37, 55, 59, 63, 78, 79, 82, 83, 86,
87, 88, 89, 90, 91, 102, 103, 159, 187, 189, 205, 207, 209, 215, 259, 269, 271,
287, 291, 293, 305, 317, 327, 329, 337, 341, 345, 353, 377, 381, 387, 399, 409,
413, 427, 429, 433, 441, 467, 489, 490, 495, 496, 501, 502, 503, 504, 513, 514]

OW_Obese_Control_2ndCat = [1, 33, 39, 46, 48, 50, 52, 68, 69, 80, 81, 84, 85, 119, 133, 165,
173, 175, 193, 197, 233, 261, 289, 295, 311, 355, 385, 393, 401, 417, 425, 481, 482,
483, 484, 487, 488, 491, 492, 509, 510, 76, 77, 155, 171, 263, 301, 303, 363, 371, 375, 511, 512, 515, 516,
517, 518, 4,13,35,38,42,43,44,45,47,49,51,53,54,56,57,58,60,61,72,73,104,105,110,
113,115,118,121,123,125,131,135,139,143,145,149,161,199,235,243,245,247,253,281,283,
297,319,335,367,395,397,403,405,411,423,431,453,455,457,459,461,471,479,480,499,
500]

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
	print("Loading...")

def getHealthStatus(patientNum, dic):
	return dic[patientNum]

#Function to update the health status column
def updateHealthStatus(df, dic):
	df["obs"] = pd.to_numeric(df["obs"])
	df["patient.number"] = pd.to_numeric(df["patient.number"])
	df["health.status"] = [getHealthStatus(x, dic) for x in df['patient.number']]
	return df

#Function to balance the data given a list with the number of patients
def balanceData(df,dic,balanceList):
	patients = dic.keys()
	print(patients)
	removePatients = [x for x in patients if x not in balanceList]
	print(removePatients)
	for patientNumber in removePatients:	
		df = df[~df['patient.number'].isin(removePatients)]
	return df
	
def getObs(fileName):
	reNum = re.search(r'_\d+$', fileName)
	return reNum.group(0)[1:]
	
def updateObs(df):
	df["obs"] = [getObs(x) for x in df['patient']]
	return df
	
def cleanDataEx(df):
	df = df.drop(df.columns[0], axis=1)
	df = df.loc[~((df['patient.number'] < 68) & (df['obs'] > 5)),:]
	#df = df.loc[~((df['health.status'] == 'disorder') & (df['obs'] > 3)),:] #Balancing 1st categorization
	return df
	
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
	
def signalFilter2_5_40Hz(df): #[f_000068 - f_000108] 2.5 - 40Hz #Fig 5_2 (41)
	colRemove = []
	for i in range(1,68): #[f_000001 - f_000067] Remove
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
	for i in range(68,109): #Rename to [f_000001 - f_000041]
		colName = "f_"
		colName +='{:06d}'.format(i)
		newcolName = "f_"
		newcolName += '{:06d}'.format(i-67)
		colRename[colName] = newcolName 
	df = df.rename(columns = colRename)
	return df

def signalFilter0_4__2_5Hz(df): #[f_000042 - f_000068] 0.4 - 2.5Hz #Fig 5_1 (27)
	colRemove = []
	for i in range(1,42): #[f_000001 - f_000041] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	for i in range(69,145): #[f_000069 - f_000144] Remove
		colName = "f_"
		colName +='{:06d}'.format(i)
		colRemove.append(colName)
	df = df.drop(colRemove, axis=1)
	#Rename the columns
	colRename = {}
	for i in range(42,69): #Rename to [f_000001 - f_000027]
		colName = "f_"
		colName +='{:06d}'.format(i)
		newcolName = "f_"
		newcolName += '{:06d}'.format(i-41)
		colRename[colName] = newcolName 
	df = df.rename(columns = colRename)
	return df

#Function that balance the data with a python dictionary with patient numbers and obs numbers
def balanceByDict(df, dictPython):
	removePatientsObs = {}
	#Iter from the dataframe
	for index, row in df.iterrows():
		#If the patientobs is not in dict or if yes but the obs is not in list from dict.
		if (int(row['patient.number']) not in dictPython) or (int(row['obs']) not in dictPython[int(row['patient.number'])] ):
			#Create a new slot for the patient.number to remove
			if int(row['patient.number']) not in removePatientsObs:
				removePatientsObs[int(row['patient.number'])] = []
			#Consider to remove the patientobs from the dataframe
			removePatientsObs[int(row['patient.number'])].append(int(row['obs']))
	print(removePatientsObs)
	#Iter to remove all the excluded patients
	for patientNumber in removePatientsObs:
		#Iter from the obs of the patient
		for obsNumber in removePatientsObs[patientNumber]:
			df = df.loc[~((df['patient.number'] == int(patientNumber)) & (df['obs'] == int(obsNumber))),:]
	return df

#Function to balance the data given a list of patient filenames
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

#Function to sort the data given a list of patient filenames
def sortByListPatientFileNames(df, listPython):
	df['patient'] = pd.Categorical(df['patient'], listPython)
	df = df.sort_values("patient")
	return df

def isPatientInList(df, listPatients, customText, patientNumber):
	if (int(patientNumber) in listPatients):
		return customText
	else:
		#print(patientNumber)
		tmpdf = df.loc[df['patient.number'] == int(patientNumber)]
		#print(tmpdf)
		for index, row in tmpdf.iterrows():
			#print(row['health.status'])
			return row['health.status']

#Function that update the health status of the patient list with an specific string.
def updateHealthStatusList(df, listPatients, customText):
	df["health.status"] = [isPatientInList(df, listPatients, customText, x) for x in df['patient.number']]
	return df


### Functions to generate Figures dataframes ###
def Fig_2EF(mainDataFrame):
	#Updates the labels according to the indicated dictionary.
	mainDataFrame = updateHealthStatus(mainDataFrame, secondLabeling)
	#Deletes records with patient.number < 68 and with > 5 obs because of repetition of the signal.
	mainDataFrame = cleanDataEx(mainDataFrame)
	#Balances or Filters the data set (if necessary).
	mainDataFrame = balanceByDict(mainDataFrame, bd.dfBalanceWaveletSegundaCatNew_0_3_40Hz)
	mainDataFrame = sortByListPatientFileNames(mainDataFrame, bd.dfBalanceWaveletSegundaCatNew_LPatientNames)
	
	#Filters wavelet transform at 0.3-40Hz.
	mainDataFrame = signalFilter0_3_40Hz(mainDataFrame)
	print(mainDataFrame)

	print("Saving file, please wait...")
	#Save the dataframe in csv format.
	mainDataFrame.to_csv("save\dfBalanceWaveletSegundaCat28022022A_0.3_40Hz_G.csv", index=False, header=True)
	
def Fig_4F(mainDataFrame):
	#Updates the labels according to the indicated dictionary.
	mainDataFrame = updateHealthStatus(mainDataFrame, secondLabeling)
	
	#Disorder
	OW2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, OW2ndCat)
	Obese2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, Obese2ndCat)
	#Health
	Control2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, Control2ndCat)
	
	#Join DataFrames
	mainDataFrame = pd.concat([OW2ndCatDataFrame, Obese2ndCatDataFrame, Control2ndCatDataFrame], ignore_index=True, sort=False)
	
	#Balances or Filters the data set (if necessary).
	mainDataFrame = balanceByDict(mainDataFrame, bd.dfControlvsSobrepesoyObesidad2daCat_0_3_40HzBalanceado)
	#print(mainDataFrame)
	#Deletes records with patient.number < 68 and with > 5 obs because of repetition of the signal.
	mainDataFrame = cleanDataEx(mainDataFrame)
	
	#Filters wavelet transform at 0.3-40Hz.
	mainDataFrame = signalFilter0_3_40Hz(mainDataFrame)
	print(mainDataFrame)

	print("Saving file, please wait...")
	#Save the dataframe in csv format.
	mainDataFrame.to_csv("save\dfControlvsSobrepesoyObesidad2daCat_0.3_40HzBalanceado_G.csv", index=False, header=True)
	
def Fig_4G(mainDataFrame):
	#Updates the labels according to the indicated dictionary.
	mainDataFrame = updateHealthStatus(mainDataFrame, secondLabeling)
	
	#Disorder
	OW2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, OW2ndCat)
	Obese2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, Obese2ndCat)
	MetS2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, MetS2ndCat)
	#Health
	Control2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, Control2ndCat)
	
	#Join DataFrames
	mainDataFrame = pd.concat([OW2ndCatDataFrame, Obese2ndCatDataFrame, MetS2ndCatDataFrame, Control2ndCatDataFrame], ignore_index=True, sort=False)
	
	#Balances or Filters the data set (if necessary).
	mainDataFrame = balanceByDict(mainDataFrame, bd.dfControlvsSobrepeso_ObesidadySM2daCat_0_3_40HzBalanceado)
	#Deletes records with patient.number < 68 and with > 5 obs because of repetition of the signal.
	mainDataFrame = cleanDataEx(mainDataFrame)
	
	#Filters wavelet transform at 0.3-40Hz.
	mainDataFrame = signalFilter0_3_40Hz(mainDataFrame)
	print(mainDataFrame)

	print("Saving file, please wait...")
	#Save the dataframe in csv format.
	mainDataFrame.to_csv("save\dfControlvsSobrepeso_ObesidadySM2daCat_0.3_40HzBalanceado_G.csv", index=False, header=True)
	
def Fig_3A(mainDataFrame):
	#Updates the labels according to the indicated dictionary.
	mainDataFrame = updateHealthStatus(mainDataFrame, secondLabeling)
	
	#Health
	Control2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, Control2ndCat)
	Control2ndCatDataFrame = updateHealthStatusList(Control2ndCatDataFrame, Control2ndCat, "health")
	#Disorder
	OW2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, OW2ndCat)
	OW2ndCatDataFrame = updateHealthStatusList(OW2ndCatDataFrame, OW2ndCat, "sobrepeso")
	Obese2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, Obese2ndCat)
	Obese2ndCatDataFrame = updateHealthStatusList(Obese2ndCatDataFrame, Obese2ndCat, "obesidad")
	DMnoDR2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, DMnoDR2ndCat)
	DMnoDR2ndCatDataFrame = updateHealthStatusList(DMnoDR2ndCatDataFrame, DMnoDR2ndCat, "diabetesSinRD")
	MetS2ndCatDataFrame = balanceData(mainDataFrame, secondLabeling, MetS2ndCat)
	MetS2ndCatDataFrame = updateHealthStatusList(MetS2ndCatDataFrame, MetS2ndCat, "MetS")
	
	#Join DataFrames
	mainDataFrame = pd.concat([Control2ndCatDataFrame, OW2ndCatDataFrame, Obese2ndCatDataFrame, DMnoDR2ndCatDataFrame, MetS2ndCatDataFrame], ignore_index=True, sort=False)
	
	#Balances or Filters the data set (if necessary).
	#mainDataFrame = balanceByDict(mainDataFrame, bd.dfControl_vs_Sobrepeso_vs_Obesidad_vs_DiabetesSinRD_vs_SM_2daCat_0_3_40HzBalanceado)
	mainDataFrame = balanceByListPatientFileNames(mainDataFrame, bd.dfControl_vs_Sobrepeso_vs_Obesidad_vs_DiabetesSinRD_vs_SM_2daCat_0_3_40HzBalanceado_LPatientNames)
	#Deletes records with patient.number < 68 and with > 5 obs because of repetition of the signal.
	mainDataFrame = cleanDataEx(mainDataFrame)
	
	#Filters wavelet transform at 0.3-40Hz.
	mainDataFrame = signalFilter0_3_40Hz(mainDataFrame)
	print(mainDataFrame)

	print("Saving file, please wait...")
	#Save the dataframe in csv format.
	mainDataFrame.to_csv("save\dfControl vs Sobrepeso vs Obesidad vs DiabetesSinRD vs SM_2daCat_0.3_40HzBalanceado_G.csv", index=False, header=True)

def Fig_5A1(mainDataFrame):
	#Updates the labels according to the indicated dictionary.
	mainDataFrame = updateHealthStatus(mainDataFrame, secondLabeling)
	#Balances or Filters the data set (if necessary).
	mainDataFrame = balanceByDict(mainDataFrame, bd.dfBalanceWaveletSegundaCat28022022A_0_4_2_5Hz)
	mainDataFrame = sortByListPatientFileNames(mainDataFrame, bd.dfBalanceWaveletSegundaCat28022022A_LPatientNames)
	#Deletes records with patient.number < 68 and with > 5 obs because of repetition of the signal.
	mainDataFrame = cleanDataEx(mainDataFrame)
	
	#Filters wavelet transform at 0.4-2.5Hz.
	mainDataFrame = signalFilter0_4__2_5Hz(mainDataFrame)
	print(mainDataFrame)

	print("Saving file, please wait...")
	#Save the dataframe in csv format.
	mainDataFrame.to_csv("save\dfBalanceWaveletSegundaCat28022022A_0.4_2.5Hz_G.csv", index=False, header=True)
	
def Fig_5A2(mainDataFrame):
	#Updates the labels according to the indicated dictionary.
	mainDataFrame = updateHealthStatus(mainDataFrame, secondLabeling)
	#Balances or Filters the data set (if necessary).
	mainDataFrame = balanceByDict(mainDataFrame, bd.dfBalanceWaveletSegundaCat28022022A_2_5_40Hz)
	mainDataFrame = sortByListPatientFileNames(mainDataFrame, bd.dfBalanceWaveletSegundaCat28022022A_LPatientNames)
	#Deletes records with patient.number < 68 and with > 5 obs because of repetition of the signal.
	mainDataFrame = cleanDataEx(mainDataFrame)
	
	#Filters wavelet transform at 2.5-40Hz.
	mainDataFrame = signalFilter2_5_40Hz(mainDataFrame)
	print(mainDataFrame)

	print("Saving file, please wait...")
	#Save the dataframe in csv format.
	mainDataFrame.to_csv("save\dfBalanceWaveletSegundaCat28022022A_2.5_40Hz_G.csv", index=False, header=True)

### Main Program ###

#Update the column with the observation number.
mainDataFrame = updateObs(mainDataFrame)

## Generate Figure dataframes ##
Fig_2EF(mainDataFrame)#Fig_4A(mainDataFrame)
#Fig_4F(mainDataFrame)
#Fig_4G(mainDataFrame)
Fig_3A(mainDataFrame)#Fig_4I(mainDataFrame)
#Fig_5A1(mainDataFrame)
#Fig_5A2(mainDataFrame)