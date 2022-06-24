#This file is used to remove data artifacts (noise) from the start and the end of the signal
import os
import sys
import time
import pandas as pd
import numpy as np
from os import listdir
from joblib import Parallel, delayed
from os.path import isfile, join, splitext

from numpy.lib.stride_tricks import as_strided

SaveFolder = "./NoiseFree/"

#Create log file
logFile = open("logExperimentos.log", 'w')

#Reads the files located in the script directory
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]

def getNoiseValues(df, tolerance):
  occurrences = df[0].value_counts(dropna=True)
  lengthdf = len(df)
  noiseValues = []
  for value in occurrences.keys():
    valueTolerance = (occurrences[value] * 100) / lengthdf
    if(valueTolerance > tolerance):
      noiseValues.append(value)
  return noiseValues
  
def removeNoiseAtStart(df, noiseValues, threshold):
  index = 0
  countThreshold = 0
  tolerance = threshold // 80
  #Iterate over each row
  for row in df.itertuples():
    #If it is not a noise value increments the counter
    if (row._1 not in noiseValues):
      countThreshold += 1
    #If it is a noise value resets the counter
    else:
	  #Tolerance of noise values for restarting the count
      tolerance -= 1
      if(tolerance < 0):
        tolerance = threshold // 80
        countThreshold = 0
    #If the counter is equal to the threshold
    if (countThreshold >= threshold):
      #Found a continuous signal without threshold length noise and with tolerance.
      return df.iloc[index-countThreshold+1:]
    index += 1
  #Otherwise the signal it's full of noise.
  return None


#Creates a the SaveFolder if doesn't exists.
if(not os.path.exists(SaveFolder)):
	os.mkdir(SaveFolder)
	print("Directory '% s' created" % SaveFolder)

#For every file obtain the patient number.
for f in arrFiles:
	fileName = splitext(f)[0]
	fileExtension = splitext(f)[1]
	#Obtain the patient number
	#Avoid python and log files
	if ".py" not in fileExtension and ".log" not in fileExtension:
		print("\n\nNew pacient read:" + f)
		logFile.write("\n\nNew pacient read:" + f + "\n")
		df = None
		df = pd.read_csv(f, header=None, engine='python')
		print("DataFrame inicial:")
		logFile.write("\n\nDataFrame inicial:")
		logFile.write("\n\n")
		logFile.write(str(df.head(10)))
		logFile.write("\n")
		logFile.write(str(df.tail(10)))
		print("File size:" + str(len(df.index)))
		logFile.write("\nFile size:" + str(len(df.index)))
		print(df)
		
		#Get df columns
		columnsDf = list(df.columns)
		columnsDf = columnsDf[1:]
		#Removes all columns except the first one
		df = df.drop(columns=columnsDf)
		#Removes strings and nulls
		df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna()
		time.sleep(0.5)
		
		dfOriginal = None
		dfOriginal = df.copy()
		time.sleep(0.5)
		
		#Obtains the most repeated values given a percentage with respect to the original signal.
		start = time.time()
		noiseValuesDf = getNoiseValues(df, 2.0)
		end = time.time()
		print("Time elapsed:", end - start, "seconds.")
		#print(getNoiseValues(df, 5.0))
		print(noiseValuesDf)
		logFile.write("\nNoise values:" + str(noiseValuesDf))
		
		start = time.time()
		startValue = 2000
		endValue = 2000
		#Remove noise at startup (until n values are found in a row that are not noise).
		df = removeNoiseAtStart(df, noiseValuesDf, startValue) #2000 noise-free values in a row.
		while(df is None and startValue > 0):
			df = dfOriginal.copy()
			time.sleep(0.5)
			startValue = startValue - 500
			df = removeNoiseAtStart(df, noiseValuesDf, startValue)
		if(startValue < 0):
			df = None
			df = dfOriginal.copy()
			time.sleep(0.5)
		end = time.time()
		print("Time elapsed:", end - start, "seconds.")

		start = time.time()
		#Inverts signal values
		cleandfS = df.copy()
		time.sleep(0.5)
		#cleandfS[:] = cleandfS[::-1]
		cleandfS = cleandfS.iloc[::-1]
		
		#Remove the noise at the end because the signal is inverted (until it finds n values in a row that are not noise).
		cleandfS = removeNoiseAtStart(cleandfS, noiseValuesDf, endValue) #2000 noise-free values in a row.
		while(cleandfS is None and endValue > 0):
			cleandfS = df.copy()
			time.sleep(0.5)
			#Inverts signal values
			#cleandfS[:] = cleandfS[::-1]
			cleandfS = cleandfS.iloc[::-1]
			endValue = endValue - 500
			#Remove noise at the end
			cleandfS = removeNoiseAtStart(cleandfS, noiseValuesDf, endValue) #2000 noise-free values in a row.
		if(endValue < 0):
			cleandfS = None
			cleandfS = df.copy()
			time.sleep(0.5)

		#Returns the values to their original position (cleandfS is inverted).
		cleandf = cleandfS.copy()
		time.sleep(0.5)
		#cleandf[:] = cleandf[::-1]
		cleandf = cleandf.iloc[::-1]
		end = time.time()
		print("Time elapsed:", end - start, "seconds.")
		
		dfFinal = None
		dfFinal = cleandf.copy()
		time.sleep(0.5)
		
		print("Final DataFrame:")
		logFile.write("\n\nFinal DataFrame:")
		print(dfFinal)
		logFile.write("\n\n")
		logFile.write(str(dfFinal.head(10)))
		logFile.write("\n")
		logFile.write(str(dfFinal.tail(10)))
		print("Final File size:" + str(len(dfFinal.index)))
		logFile.write("\nFinal size:" + str(len(dfFinal.index)))
		logFile.write("\n")
		dfFinal.to_csv(SaveFolder + f, index=False, header=False)

		
logFile.close()
