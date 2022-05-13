#This script is used to calculate the wavelet transform 
#for each patient given their ERG signal.
import cwt
import pandas as pd
import numpy as np
import statistics

import re
import sys
import time
import pandas as pd
import numpy as np
from os import listdir
from joblib import Parallel, delayed
from os.path import isfile, join, splitext
import multiprocessing

start = time.time()
def loop(arrFiles, idWorker):
    #Define the column names of the final dataframe.
    dfColumnNames = ["patient","patient.number","obs","health.status","group"]

    #Assign a label for each patient (optional)
    PATIENTS = {1:'disorder',2:'disorder',3:'disorder',
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

    #Initializes the columns of the wavelet transform.
    for i in range(1,145):
        columnName = "f_"
        columnName +='{:06d}'.format(i)
        dfColumnNames.append(columnName)
        
    dfAllWavelet = pd.DataFrame(columns = dfColumnNames)

    print(dfAllWavelet.columns)

    #Reads the files located in the script directory
    for f in arrFiles:
        fileName = splitext(f)[0]
        fileExtension = splitext(f)[1]
        #csv files only
        if ".csv" in fileExtension: 
            print("Reading and preprocesing file: " + f)
            #try:
            if ".csv" in fileExtension: 
                #Read the csv file
                dfPatient = pd.read_csv(f, header=None)
                #Gets the file size
                print("File size:" + str(len(dfPatient.index)))
                #It is converted to a one-dimensional numpy array.
                dfPatient = dfPatient.to_numpy()
                dfPatient_1d = dfPatient.flatten()
                
                #Obtains the wavelet transform given the ERG signal of the patient.
                fs = 1000
                coeff, freq = cwt.cwt(dfPatient_1d, 'morl', sampling_frequency=fs)
                
                #power = (abs(wt).^2);
                opone = lambda x: abs(x)*abs(x)
                oponefunc = np.vectorize(opone)
                coeff1 = oponefunc(coeff)
                
                #meanSpectrum = mean(power, 2);
                #x = statistics.mean(data1)
                listaMean = []
                for element in coeff1:
                    meanElement = statistics.mean(element)
                    listaMean.append(meanElement)

                print(len(listaMean))
                
                listaMean = listaMean[::-1]

                print(len(fLinear))
                print(len(listaMean))
                
                #Obtain the patient number
                patientNumber = None
                res = re.search('\d{2,4}', fileName)

                if res is not None:
                    patientNumber = int(res.group(0))
                print("patientNumber:" + str(patientNumber))
                fileNameClean = fileName.strip()
                fileNameClean = fileNameClean.replace(" ", "")
                fileNameClean = fileNameClean.lower()
                
                #Generates a new row with the generated wavelet data
                listaMean.insert(0, "none") #group
                listaMean.insert(0, PATIENTS[int(patientNumber)]) #health.status
                listaMean.insert(0, "-") #obs
                listaMean.insert(0, str(patientNumber)) #patient.number
                listaMean.insert(0, fileNameClean) #patient (filename)
                    
                dfAllWavelet.loc[-1] = listaMean  # adding a row
                dfAllWavelet.index = dfAllWavelet.index + 1  # shifting index
                dfAllWavelet = dfAllWavelet.sort_index()  # sorting by index
                    
            #except:
                #print("Unexpected error for file: " + f + "\n", sys.exc_info())
            
    print(dfAllWavelet)
    dfAllWavelet.index = np.arange(1, len(dfAllWavelet) + 1)
    dfAllWavelet.to_csv("dfAllWavelet" + str(idWorker) + ".csv", index=True, header=True)

### Main program ###

arrFilesGlobal = [f for f in listdir(".") if isfile(join(".", f))]
arrFilesGlobal = np.array(arrFilesGlobal)

#Obtains the number of workers
workers = multiprocessing.cpu_count()

#Divide the work among the workers
arrFilesTemp = np.array_split(arrFilesGlobal, workers)
arrFilesSplit = []
for e in arrFilesTemp:
    arrFilesSplit.append(e.tolist())

#Parallel(n_jobs=-1, verbose=10)(delayed(loop)(arrFiles) for arrFiles in arrFilesSplit)
Parallel(n_jobs=-1, verbose=10)(delayed(loop)(arrFilesSplit[i], i) for i in range(len(arrFilesSplit)) )
end = time.time()
print("Total time in seconds//:", end - start)