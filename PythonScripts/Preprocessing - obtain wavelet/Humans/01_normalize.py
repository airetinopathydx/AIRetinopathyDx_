#This file is used to normalize the signal [-1000,1000] with the MinMax formula.
import os
import sys
import time
import pandas as pd
import numpy as np
from os import listdir
from joblib import Parallel, delayed
from os.path import isfile, join, splitext

from numpy.lib.stride_tricks import as_strided

SaveFolder = "./NormalizedFiles/"

#Create log file
logFile = open("logNorm.log", 'w')

#Reads the files located in the script directory
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]
  
def minMax(df, a, b):
	#Min max formula [a, b]
	minX = float(df.min())
	maxX = float(df.max())
	return df.apply( lambda x: a + ( ((x - minX) * (b-a)) / (maxX - minX) ) )

#Creates a the SaveFolder if doesn't exists.
if(not os.path.exists(SaveFolder)):
	os.mkdir(SaveFolder)
	print("Directory '% s' created" % SaveFolder)

#For every file obtain the patient number.
for f in arrFiles:
	fileName = splitext(f)[0]
	fileExtension = splitext(f)[1]
	#Obtain the patient number
	#Avoid python and excel 2007 or later files
	if ".py" not in fileExtension and ".log" not in fileExtension:
		print("\n\nNew pacient read:" + f)
		logFile.write("\n\nNew pacient read:" + f + "\n")
		df = None
		df = pd.read_csv(f, header=None, engine='python')
		print("Initial DataFrame:")
		logFile.write("\n\nInitial DataFrame:")
		logFile.write("\n\n")
		logFile.write(str(df.head(10)))
		logFile.write("\n")
		logFile.write(str(df.tail(10)))
		print("File size:" + str(len(df.index)))
		logFile.write("\nFile size:" + str(len(df.index)))
		print(df)
		
		#Applies the MinMax formula to the dataframe.
		dfFinal = minMax(df, -1000, 1000)
		
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
