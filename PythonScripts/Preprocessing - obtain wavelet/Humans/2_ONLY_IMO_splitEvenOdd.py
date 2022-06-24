#This file is used to split the signal in even and odd values and to save it in separated files.
#It is used in some IMO patients.
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
    if (fileExtension == ".py"):
        continue
    print("Reading and converting file: " + f)
    try:
        #Read the csv file
        df = pd.read_csv(f, header=None)
        #Removes strings and nulls
        df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna()
        #Gets the odd and even rows
        df_even = df.iloc[::2]
        df_odd = df.iloc[1::2]
        #Save csv files
        df_even.to_csv(fileName + "_even" + fileExtension, index=False, header=False)
        df_odd.to_csv(fileName + "_odd" + fileExtension, index=False, header=False)
    except:
        print("Unexpected error for file: " + f + "\n", sys.exc_info())
