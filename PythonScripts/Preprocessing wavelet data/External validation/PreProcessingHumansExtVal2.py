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
secondLabelingExtVal = {1:'disorder',2:'disorder',3:'disorder',
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
    109:'disorder',110:'health',111:'disorder',112:'disorder',
    113:'health',114:'health',
    115:'health',116:'health',117:'health',
    118:'health',119:'disorder',120:'disorder',121:'health',
    122:'health',
    123:'health',124:'health',
    125:'health',126:'health', 127:'disorder',
    128:'disorder',129:'disorder', 130:'disorder',
    131:'health',132:'health',
    133:'disorder',134:'disorder',
    135:'health',136:'health',137:'disorder',138:'disorder',
    139:'health',140:'health',
    141:'disorder',142:'disorder',
    143:'health',144:'health',145:'health',146:'health',
    147:'disorder',148:'disorder',
    149:'health',150:'health',
    151:'health',152:'health',153:'disorder',154:'disorder',
    155:'disorder',156:'disorder',
    157:'disorder',158:'disorder',
    159:'disorder',160:'disorder',
    161:'health',162:'health',
    163:'disorder',164:'disorder',
    165:'disorder',166:'disorder',
    167:'disorder',168:'disorder',
    169:'disorder',170:'disorder',
    171:'disorder',172:'disorder',
    173:'disorder',174:'disorder',
    175:'disorder',176:'disorder',
    177:'disorder',178:'disorder',
    179:'disorder',180:'disorder',
    181:'disorder',182:'disorder',
    183:'disorder',184:'disorder',
    185:'disorder',186:'disorder',
    187:'disorder',188:'disorder',
    189:'disorder',190:'disorder',
    191:'disorder',192:'disorder',
    193:'disorder',194:'disorder',
    195:'disorder',196:'disorder',
    197:'disorder',198:'disorder',
    199:'health',200:'health',
    201:'disorder',202:'disorder',
    203:'disorder',204:'disorder',
    205:'disorder',206:'disorder',
    207:'disorder',208:'disorder',
    209:'disorder',210:'disorder',
    211:'disorder',212:'disorder',
    213:'disorder',214:'disorder',
    215:'disorder',216:'disorder',
    217:'disorder',218:'disorder',
    219:'disorder',220:'disorder',
    221:'disorder',222:'disorder',
    223:'disorder',224:'disorder',
    225:'disorder',226:'disorder',
    227:'disorder',228:'disorder',
    229:'disorder',230:'disorder',
    231:'disorder',232:'disorder',
    233:'disorder',234:'disorder',
    235:'health',236:'health',
    237:'disorder',238:'disorder',
    239:'disorder',240:'disorder',
    241:'disorder',242:'disorder',
    243:'health',244:'health',
    245:'health',246:'health',
    247:'health',248:'health',
    249:'disorder',250:'disorder',
    251:'disorder',252:'disorder',
    253:'health',254:'health',
    255:'disorder',256:'disorder',
    257:'disorder',258:'disorder',
    259:'disorder',260:'disorder',
    261:'disorder',262:'disorder',
    263:'disorder',264:'disorder',
    265:'disorder',266:'disorder',
    267:'disorder',268:'disorder',
    269:'disorder',270:'disorder',
    271:'disorder',272:'disorder',
    273:'disorder',274:'disorder',
    275:'disorder',276:'disorder',
    277:'disorder',278:'disorder',
    279:'disorder',280:'disorder',
    281:'health',282:'health',
    283:'health',284:'health',
    285:'disorder',286:'disorder',
    287:'disorder',288:'disorder',
    289:'disorder',290:'disorder',
    291:'disorder',292:'disorder',
    293:'disorder',294:'disorder',
    295:'disorder',296:'disorder',
    297:'health',298:'health',
    299:'disorder',300:'disorder',
    301:'disorder',302:'disorder',
    303:'disorder',304:'disorder',
    305:'disorder',306:'disorder',
    307:'disorder',308:'disorder',
    309:'disorder',310:'disorder',
    311:'disorder',312:'disorder',
    313:'disorder',314:'disorder',
    315:'disorder',316:'disorder',
    317:'disorder',318:'disorder',
    319:'health',320:'health',
    321:'disorder',322:'disorder',
    323:'disorder',324:'disorder',
    325:'disorder',326:'disorder',
    327:'disorder',328:'disorder',
    329:'disorder',330:'disorder',
    331:'disorder',332:'disorder',
    333:'disorder',334:'disorder',
    335:'health',336:'health',
    337:'disorder',338:'disorder',
    339:'disorder',340:'disorder',
    341:'disorder',342:'disorder',
    343:'disorder',344:'disorder',
    345:'disorder',346:'disorder',
    347:'disorder',348:'disorder',
    349:'disorder',350:'disorder',
    351:'disorder',352:'disorder',
    353:'disorder',354:'disorder',
    355:'disorder',356:'disorder',
    357:'disorder',358:'disorder',
    359:'disorder',360:'disorder',
    361:'disorder',362:'disorder',
    363:'disorder',364:'disorder',
    365:'disorder',366:'disorder',
    367:'health',368:'health',
    369:'health',370:'health',
    371:'disorder',372:'disorder',
    373:'disorder',374:'disorder',
    375:'disorder',376:'disorder',
    377:'disorder',378:'disorder',
    379:'disorder',380:'disorder',
    381:'disorder',382:'disorder',
    383:'disorder',384:'disorder',
    385:'disorder',386:'disorder',
    387:'disorder',388:'disorder',
    389:'disorder',390:'disorder',
    391:'disorder',392:'disorder',
    393:'disorder',394:'disorder',
    395:'health',396:'health',
    397:'health',398:'health',
    399:'disorder',400:'disorder',
    401:'disorder',402:'disorder',
    403:'health',404:'health',
    405:'health',406:'health',
    407:'disorder',408:'disorder',
    409:'disorder',410:'disorder',
    411:'health',412:'health',
    413:'disorder',414:'disorder',
    415:'disorder',416:'disorder',
    417:'disorder',418:'disorder',
    419:'disorder',420:'disorder',
    421:'health',422:'health',
    423:'health',424:'health',
    425:'disorder',426:'disorder',
    427:'disorder',428:'disorder',
    429:'disorder',430:'disorder',
    431:'health',432:'health',
    433:'disorder',434:'disorder',
    435:'disorder',436:'disorder',
    437:'disorder',438:'disorder',
    439:'disorder',440:'disorder',
    441:'disorder',442:'disorder',
    443:'disorder',444:'disorder',
    445:'disorder',446:'disorder',
    447:'disorder',448:'disorder',
    449:'disorder',450:'disorder',
    451:'disorder',452:'disorder',
    453:'health',454:'health',
    455:'health',456:'health',
    457:'health',458:'health',
    459:'health',460:'health',
    461:'health',462:'health',
    463:'health',464:'health',
    465:'disorder',466:'disorder',
    467:'disorder',468:'disorder',
    469:'disorder',470:'disorder',
    471:'health',472:'health',
    473:'disorder',474:'disorder',
    475:'disorder',476:'disorder',
    477:'disorder',478:'disorder',
    479:'health',480:'health',481:'disorder',482:'disorder',
    483:'disorder',484:'disorder',487:'disorder',488:'disorder',
    489:'disorder',490:'disorder',491:'disorder',492:'disorder',
    493:'disorder',494:'disorder',495:'disorder',496:'disorder',
    497:'disorder',499:'health',500:'health',501:'disorder',
    502:'disorder',503:'disorder',504:'disorder',505:'disorder',
    506:'disorder',507:'disorder',508:'disorder',509:'disorder',
    510:'disorder',511:'disorder',512:'disorder',513:'disorder',
    514:'disorder',515:'disorder',516:'disorder',517:'disorder',
    518:'disorder',519:'disorder',520:'disorder',529:'disorder',
    530:'disorder',531:'disorder',532:'disorder',533:'disorder',
    534:'disorder',535:'disorder',
    662:'disorder',663:'disorder',
    672:'disorder',673:'disorder',
    674:'disorder',675:'disorder',
    680:'disorder',681:'disorder',
    682:'disorder',683:'disorder',
    684:'disorder',685:'disorder',
    688:'health',699:'health',
    700:'health',701:'health',
    704:'disorder',705:'disorder',
    706:'disorder',707:'disorder',
    708:'disorder',709:'disorder',
    710:'disorder',711:'disorder'}

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
	randomNumber = random.randint(0, tmpdf.shape[0]-1)
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

#Filter the defined range of values of the signal.
mainDataFrame = signalFilter0_3_40Hz(mainDataFrame)
print(mainDataFrame)

#Auto balance the dataset randomly
mainDataFrame = autoBalanceClasses(mainDataFrame)
print(mainDataFrame)

#Save the dataframe in csv format.
mainDataFrame.to_csv("save\dfNewExperimentValidationData_0.3_40Hz_Balanced.csv", index=False, header=True)