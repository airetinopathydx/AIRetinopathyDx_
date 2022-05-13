#This file is used to split the data in fragments of 60 seconds and restrict to -900 to 900 values.
import sys
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join, splitext

#Reads the files located in the script directory
arrFiles = [f for f in listdir(".") if isfile(join(".", f))]

for f in arrFiles:
    fileName = splitext(f)[0]
    fileExtension = splitext(f)[1]
    #Avoid python files
    if (fileExtension == ".py" and fileExtension == ".xlsx"):
        continue
    print("Reading and converting file: " + f)
    try:
        #Read the csv file
        df = pd.read_csv(f, header=None)
        #Gets file size with filtered values
        print("File size before filter:" + str(len(df.index)))
        columnsDf = list(df.columns)
        columnsDf = columnsDf[1:]
        #Removes all columns except the first one
        df = df.drop(columns=columnsDf)
        #Removes strings and nulls
        df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna()
        #Filter values
        df = df[(df[0] >= -900)  & (df[0] <= 900)]
        #Gets file size with filtered values
        print("File size after filter:" + str(len(df.index)))
        #Divides into files of 60,000 rows each
        for i in range(0, len(df.index)//60000):
            #Splits the data into a new dataframe
            new_df = df.iloc[i*60000:(i+1)*60000:1]
            #Save the data in a csv file
            #new_df.to_excel(fileName + "_" + str(i+1) + ".xlsx", index=False, header=False)
            new_df.to_csv(fileName + "_" + str(i+1) + ".csv", index=False, header=False)
    except:
        print("Unexpected error for file: " + f + "\n", sys.exc_info())