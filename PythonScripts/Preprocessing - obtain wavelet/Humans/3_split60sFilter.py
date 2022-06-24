#This file is used to split the each file in individual files of 60 seconds (60,000 rows).
import sys
import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join, splitext

SaveFolder = "./Split60sPatients/"

#Reads the files located in the script directory
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]

#Creates a the SaveFolder if doesn't exists.
if(not os.path.exists(SaveFolder)):
	os.mkdir(SaveFolder)
	print("Directory '% s' created" % SaveFolder)

for f in arrFiles:
    fileName = splitext(f)[0]
    fileExtension = splitext(f)[1]
    #Avoid python and excel 2007 or later files
    if (fileExtension == ".py" and fileExtension == ".xlsx"):
        continue
    print("Reading and converting file: " + f)
    try:
        #Read the csv file
        df = pd.read_csv(f, header=None)
        #Gets file size with filtered values
        print("File size:" + str(len(df.index)))
        #Divides into files of 60,000 rows each
        for i in range(0, len(df.index)//60000):
            #Splits the data into a new dataframe
            new_df = df.iloc[i*60000:(i+1)*60000:1]
            #Save the data in a csv file
            #new_df.to_excel(fileName + "_" + str(i+1) + ".xlsx", index=False, header=False)
            new_df.to_csv(SaveFolder + fileName + "_" + str(i+1) + ".csv", index=False, header=False)
    except:
        print("Unexpected error for file: " + f + "\n", sys.exc_info())
