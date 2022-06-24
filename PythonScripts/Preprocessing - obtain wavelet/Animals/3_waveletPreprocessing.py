#This script is used to calculate the wavelet transform 
#for each file.
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
                
                #Obtains the wavelet transform given the ERG signal of the animal.
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

                #print(listaMean)
                print(len(listaMean))
                
                listaMean = listaMean[::-1]

                print(len(listaMean))
                
                #Obtain the patient number (optional in animals)
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
                listaMean.insert(0, "unknown") #health.status
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
    dfAllWavelet.to_csv("dfAllWavelet" + str(idWorker) + ".csv", index=False, header=True)

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

Parallel(n_jobs=-1, verbose=10)(delayed(loop)(arrFilesSplit[i], i) for i in range(len(arrFilesSplit)) )
end = time.time()
print("Total time in seconds//:", end - start)
