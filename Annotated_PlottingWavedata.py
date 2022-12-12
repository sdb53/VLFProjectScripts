"""
This file reads in the text file created in the data reading script and uses it to plot the time spectrum. We also include our first attempts of plotting a FFT and spectrogram.
"""

import numpy as np
from numpy import fft
import glob
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import re


wavedata = np.loadtxt("File_name.txt") #Reading in the combined waveformdata 

file_t_start = "First file in time range" #obtaining the start time (of sampling) from the first file...
data_t_start = np.load(file_t_start, allow_pickle=True).item()
t_start = data_t_start[0]["starttime"] #...from the fist waveform

file_t_end = "Last file in time range" #obtaining the end time (of sampling) from the last file...
data_t_end = np.load(file_t_end, allow_pickle=True).item()
t_end = data_t_end[6407]["endtime"] #...from the final waveform

dt = np.timedelta64(int(data_t_start[0]["smplint"] * 1e9), "ns") #obtaining the sample interval (in nanoseconds) - constant throughout

t = np.arange(t_start, t_end - (6165*dt), dt) #to match len(waveforms) to len(t). Need to play around with this number as the number of waveforms varies in each file.


#Plotting the (combined) waveform data in the time dependent regime
plt.figure(figsize=(16, 6), dpi =150)
plt.plot(t, wavedata)
plt.xlabel("time")
plt.ylabel("ADC counts")
plt.title("Title")
plt.savefig("")
plt.show()

FFTwaveforms = abs(fft.fft(wavedata)) #Applying Fourier Transform to the (combined) waveform data
freq = fft.fftfreq(len(wavedata), data_t_start[0]["smplint"]) #sets up frequency bins

#Plotting the (combined) waveform data in the frequency dependent regime
plt.figure(figsize=(8, 6), dpi = 150)
plt.plot(freq, FFTwaveforms)
plt.xlabel("freq")
plt.ylabel("FFT")
plt.title("Title")
plt.savefig("")
plt.show()
    
    
sample_freq, segment_time, sxx = signal.spectrogram(wavedata, 1/(data_t_start[0]["smplint"])) #Attributing values to spectrogram parameters #sample rate = 109.375 kHz

                                                                           
#Plotting the (combined) waveform data as a spectrogram (a visual representation of the signal's spectrum of frequencies as it varies with time)
plt.pcolormesh(segment_time, sample_freq, np.log(sxx), shading = 'gouraud')
plt.xlabel("time (s)")
plt.ylabel("freq (Hz)")
plt.axvline(300, linestyle = '--', color = 'white') #highlihting the earthquake's position
plt.title("Title")
plt.savefig("")
plt.colorbar(label = 'Relative Intensity')
plt.show() 
