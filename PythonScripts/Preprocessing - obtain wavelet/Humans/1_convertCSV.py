#This file is used to convert xslx files to csv.
import sys
import time
import pandas as pd
import numpy as np
from os import listdir
from joblib import Parallel, delayed
from os.path import isfile, join, splitext

#Reads the files located in the script directory
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]
filesToRead = []

for f in arrFiles:
	fileName = splitext(f)[0]
	fileExtension = splitext(f)[1]
	#Avoid python and excel 2007 or later files
	if ".py" not in fileExtension: 
		filesToRead.append(f)


start = time.time()
def loop(fileName):
	print("Reading file: " + fileName)
	try:
		#Read the file in Excel format
		df = pd.read_excel(fileName,engine='openpyxl', header=None)
		df.to_csv(splitext(fileName)[0] + ".csv", index=False, header=False)
	except:
		print("Unexpected error for file: " + fileName + "\n", sys.exc_info())
    
Parallel(n_jobs=-1, verbose=10)(delayed(loop)(fileName) for fileName in filesToRead)
end = time.time()
print("Excel//:", end - start)