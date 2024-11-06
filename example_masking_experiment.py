### Example Masking Experiment ###

'''
This script simulates an auditory masking experiment using a notched-noise method to explore critical bands.

The goal is to demonstrate how the masking effect of the noises changes with different notch widths
(while their intensities remain roughly the same) around a fixed pure tone, which is the target to be masked.

       amplitude
           |       _____           _____
           |      |     |         |     |
           |      |     |    |    |     |
           |      |     |    |    |     |
           |______|_____|____|____|_____|______ frequency
                         <--...-->

* RUNNING THIS SCRIPT PLAYS SOUNDS FROM YOUR DEVICE WHICH MAY BE LOUD *
'''

from psychoacoustics_functions import *
import numpy as np

tone_freq = 1000  # the frequency of the target pure tone
noise_band = 200  # the width of the noise bands (which symmetrically surround the tone frequency)

silence1 = sines(0, l=.5)  # a silent segment of 0.5 seconds
silence2 = sines(0, l=.1)  # a silent segment of 0.1 seconds
target = sines(tone_freq, l=.5)  # a pure tone of 'tone_freq' Hz lasting 0.5 seconds
target = adjust(target)  # to prevent clicking sounds when the target starts and ends
target = adjust_amp(target, -16)  # changes the target's amplitude by dBs

comb = np.concatenate((silence1, target))  # combines the initial silent segment and the pure tone

noises = []
for i in [1000, 500, 300, 200, 150, 100, 70, 50, 30]:  # iterates over different notch widths
    noises.append(adjust(noise([[tone_freq-i/2-noise_band, tone_freq-i/2], 
                                [tone_freq+i/2, tone_freq+i/2+noise_band]], 
                                l=1)))  # the notched noise signals, each with a duration of 1 second

print(f'Average noise RMS intensity: {round(np.mean([intensity(i) for i in noises]), 3)}')
print(f'Target RMS intensity: {round(intensity(target), 3)}\n')

if input('To continue to hear the experiment sounds, press "Y": ')=='Y':
    for i in range(len(noises)):  # iterates through each noise signal and plays it, followed by the target tone
        play(noises[i]+comb)  # len(noises[i]) = len(silence1) + len(target)
        play(silence2)  # adds a brief silence in between
