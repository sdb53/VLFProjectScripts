"""
Annotated Spectrogram and FFT plotter with frequency bin analysis. Source code from gmarlton from met office, many thanks for your help with this Graham!
"""
"""
Created on Thu May 12 16:42:45 2022

@author: gmarlton
"""

import numpy as np
import glob
import sys
from scipy import fft
import matplotlib.pyplot as plt

        
VLF_TX = {"Cutler":{"P":2e6, "f" : 24e3},  #Power and frequency of transmitters for accessing frequency bins
          "Anthorn":{"P" : 550e3, "f" : 19.58e3}, 
          "St Assise":{"P" : 23e3, "f" : 20.9e3},
          "Rhauderfehn":{"P" : 800e3, "f" : 23.4e3},
          "Lamoure":{"P" : 250e3, "f" : 25.2e3},
          "Rosnay":{"P" : 400e3, "f" : 21.75e3},
          "Tavolara":{"P" : 43e3, "f" : 20.27e3}, 
	      "Bafa":{"P" : 100e3, "f" : 26.7e3}, 
	      "Noviken":{"P" : 45e3, "f" : 16.4e3}, 
	      "Grindavik":{"P" : np.nan, "f" : 37.5e3}}

data_out = [] 


start_time = "2022-01-11T12:40:00"# Edit this for the start time - will be used to set up time axis
end_time = "2022-01-11T12:50:00"# Edit this for the end time - will be used to set up time axis


study_times_files = np.arange(np.datetime64(start_time), #Making an array containing time for each minute in datatime64 form for accessing each file in the 10 min period
                        np.datetime64(end_time),
                        np.timedelta64(1, "m"))




study_time_array = np.arange(np.datetime64(start_time), #Making an array for each second to use as the time axis in the plots
                        np.datetime64(end_time),
                        np.timedelta64(1, "s"))

# Compute this once!
fft_freq = fft.fftfreq(1024, 1 / 109375.0)[:512] #Setting up frequency bins

node = "569218Q0B00170029"# Edit this to the node of the receiver in question
spectogram = np.zeros((len(study_time_array), 512)) #Spectrogram 2D array
waveform_store = {"waveforms":[], "t":[], "fft": []} #Dictionary for storing the data

for study_time in study_times_files: #Looping through files in the 10 minute period
    
    peak_out = []
    peak_out_time = [] 
    time_string = study_time.astype("datetime64[Y]").astype(str) + \
        study_time.astype("datetime64[M]").astype(str)[-2:] + \
        study_time.astype("datetime64[D]").astype(str)[-2:] + \
        study_time.astype("datetime64[h]").astype(str)[-2:] + \
        study_time.astype("datetime64[m]").astype(str)[-2:]
#Creating the time string to access each file in the 10 minutes
   
    filename = "Payerne" + "_" + node + "." + \
               time_string + ".npy" # Selecting the files - files all have the form Payerne_569218Q0B00170029.202201111247. So we have place name, followed the the node, then the time string, then npy.
                   
    file_list = glob.glob(filename) #Adding the file just read in above to the files list
        
    if len(file_list) == 1: #When there is a file in the file_list (not before) read in the waveforms
        waveforms = np.load(file_list[0], allow_pickle=True).item()
        
        for idx in waveforms: #Reading out the start time and waveform data from all 6408 (some 6415) waveforms
            waveform_store["t"].append(
                waveforms[idx]["starttime"] #Append the start time to the dictionary
                )
            waveform_store["fft"].append(
                np.abs(fft.fft(waveforms[idx]["wvfmdata"])[:512]) #Append the fast fourier transformed waveform data (ADC counts) to the dictionary
                )

#Data from all the files in the time period specified in lines 31 and 32 have now been read in 

waveform_store["t"] = np.array(waveform_store["t"])  #Read out the start time from each file as an array
waveform_store["fft"] = np.array(waveform_store["fft"]) #Read out fourier transformed data as an array

for ii, time_window in enumerate(study_time_array): #Appending data into arrays to get into form required by countorf function used in line 95
    l1 = np.where(waveform_store["t"].astype("datetime64[s]") == time_window)[0]
    
    for jj in l1:
        spectogram[ii, :] = spectogram[ii, :] + waveform_store["fft"][jj, :]
    
    spectogram[ii, :] = spectogram[ii, :] / len(l1)

plt.figure(figsize=(12, 8), dpi = 300) #Plotting the spectrogram
ax = plt.subplot(position=[0.1,0.1,0.7,0.7])
arr = ax.contourf(study_time_array, fft_freq, np.transpose(np.log10(spectogram)))
ax.set_xlabel("UTC DD HH:MM")
ax.set_ylabel("Frequency (Hz)")
cax = plt.colorbar(mappable=arr)
cax.set_label(r'Log$_{10}$ Spectral Power')
ax.set_title("Payerne")

plt.figure(figsize=(12, 8), dpi = 300) #Plotting the fourier transform on a log-scale in the y-axis
ax1 = plt.subplot(position=[0.1,0.1,0.7,0.7])
arr1 = plt.plot(fft_freq, np.log10(abs(fft.fft(waveforms[idx]["wvfmdata"]))[:512])) 
ax1.set_ylabel("FFT")
ax1.set_xlabel("Frequency (Hz)")
ax1.set_title("Payerne")


#Transmitter names and frequencies in lists so can plot in a loop easily
transmitter = ["Cutler", "Anthorn", "St Assise", "Rhauderfehn", "Lamoure", "Rosnay", "Tavolara", "Bafa", "Noviken", "Grindavik"]
trans_freq = [24e3, 19.58e3, 20.9e3, 23.4e3, 25.2e3, 21.75e3, 20.27e3, 26.7e3, 16.4e3, 37.5e3] 

n = 0 #counter

plt.figure(figsize=(12, 8), dpi = 300)
ax2 = plt.subplot(position=[0.1,0.1,0.7,0.7])
for n in range(len(trans_freq)): #looping through the lists for each transmitter
    out = np.where(fft_freq >= trans_freq[n])[0][0] #Finding the frequency bin for the transmitters
    arr2 = plt.plot(study_time_array, spectogram[:,out], label = transmitter[n]) #Plotting the relative intensity of the frequency bin v time
    ax2.legend(fontsize = "small")
    ax2.set_ylabel("FFT")
    ax2.set_xlabel("UTC DD HH:MM")
    ax2.set_title("Payerne 11-01-2022")
    n = n + 1


        
            
    
    

        
            
            
            
        




    