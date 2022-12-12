"""
Code used for writing all the waveform data from a set of files to a separate text file, to be read in and used in plotting the time domain spectrum
"""

import numpy as np
import glob
from numpy import fft
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import pickle

files = glob.glob("File_names*.npy") #Load in globally all the files following the set naming covention
w_number = 0 #Counter to loop through all the waveforms
data = open("Combined_text_file.txt", 'w') #Opening a new text file

for file in files: #Looping through all the files
    waveforms = np.load(file, allow_pickle=True).item() #Reading in the file data as a dictionary 
    for w_number in range(len(waveforms)): #Looping through all the waveforms
        np.savetxt(data, waveforms[w_number]['wvfmdata']) #Saving the waveform data to the text file for each waveform
        w_number=w_number + 1 
                
data.close() 