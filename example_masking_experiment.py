### Example Masking Experiment ###

'''
This script simulates an auditory masking experiment using a notched-noise method to explore critical bands.
The goal of this experiment is to demonstrate how the masking effect changes with varying notch widths around a target pure tone.

* RUNNING THIS SCRIPT PLAYS SOUNDS FROM YOUR DEVICE WHICH MAY BE LOUD *
'''

from psychoacoustics_functions import *
import numpy as np

tone_freq = 1000  # the frequency of the target pure tone
noise_band = 250  # the width of the noise bands (which symmetrically surround the tone frequency)

segment1 = sines(0, l=.5)  # a silent segment of 0.5 seconds
segment2 = adjust(sines(tone_freq, l=.5))  # a pure tone of 'tone_freq' Hz lasting 0.5 seconds
segment3 = sines(0, l=.1)  # a silent segment of 0.1 seconds

tone = np.concatenate((segment1, segment2))  # concatenates the initial silent segment and the pure tone
tone = adjust_amp(tone, -20)  # lowers the amplitude of the combined tone signal by 20 dB

noises = []
for i in [1000, 500, 300, 200, 150, 100, 70, 50, 30]:  # iterates over different notch widths
    noises.append(noise([[tone_freq-i/2-noise_band, tone_freq-i/2], 
                         [tone_freq+i/2, tone_freq+i/2+noise_band]], l=1))  # the notched noise signals with a duration of 1 second

if input('To continue to hear the experiment sounds, press "Y": ')=='Y':
    for i in range(len(noises)):  # iterates through each noise signal and plays it, followed by the target tone
        play(noises[i]+tone)
        play(segment3)  # adds a brief silence in between