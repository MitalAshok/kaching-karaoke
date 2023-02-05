# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 03:08:16 2023

@author: Alice
"""

import sounddevice as sd
import numpy as np
import math
import time
from scipy.signal.windows import hann
from librosa import hz_to_note, hz_to_midi
from globalstate import pitchshifter_ready, pitchshiftby
from midi_parser import time_list, notes_list

start_time = time.time()

duration = 180  # seconds
Fs = 48000
block_size = 4096

serial_enable = True

block_dur = block_size / Fs  # s
time_axis = np.linspace(0, block_size/Fs, block_size, endpoint=False)

print(sd.default.latency)

min_note_freq = 80
max_note_freq = 600

min_note_bin = round((min_note_freq / Fs) * block_size)
max_note_bin = round((max_note_freq / Fs) * block_size)

microstep = 16
steps_per_rev = 200
mm_per_rev = 8

num_axes = 3

hann_window = hann(block_size)

machine_pp_unit = microstep * steps_per_rev / mm_per_rev

machine_limits = np.array([50, 50, 25])
machine_safety = 10

data_freq_list = []
data_list = []
note_indices = []

freq_upscale_factor = 2


def bin_to_note(bin):
    freq = (bin/block_size) * Fs
    midi_zero_freq = 8.18
    semitones_from_zero = round(12 * math.log2(freq/midi_zero_freq))

    return semitones_from_zero


def detect_main_notes(data):
    thresh = 0.1

    data_freq = np.fft.fft(data)
    main_notes = np.zeros(3)

    for i in range(num_axes):
        max_amp_bin = np.argmax(
            np.abs(data_freq[min_note_bin:max_note_bin])) + min_note_bin
        if np.abs(data_freq[max_amp_bin]) <= thresh:
            main_notes[i] = 0
        else:
            # Perform fine interpolation
            peak_data = data_freq[max_amp_bin-2:max_amp_bin+3]  # 5 points
            coeff = np.polyfit(
                np.arange(max_amp_bin-2, max_amp_bin+3), peak_data, 2)
            true_peak = -np.real(coeff[1]/(2 * coeff[0]))
            print(f"Coarse peak: {max_amp_bin}, true peak: {true_peak}")

            if int(round(true_peak)) != max_amp_bin:
                note = (true_peak/block_size) * Fs
            else:
                note = (max_amp_bin/block_size) * Fs
            main_notes[i] = note

        data_freq[max_amp_bin-10:max_amp_bin+10] = 0

    return np.array(main_notes)


def callback(indata, outdata, frames, time_s, status):
    if status:
        print(status)

    if indata.shape[0] == 0:
        return

    outdata[:] = indata
    main_notes = detect_main_notes(np.clip(indata[:, 0] * hann_window, -1, 1))
    main_notes *= freq_upscale_factor
    #print(f"Main freq: {main_notes}")

    main_note = main_notes[0]
    if main_note > 0:
        print(hz_to_note(main_note))
        global pitchshifter_ready
        #while not pitchshifter_ready:
            #print("gonna sleep")
        #    time.sleep(0.01)
        compare_note = 0
        print("comparing soon")
        for i in range(len(time_list)):
            time_elapsed = time.time() - start_time
            if time_elapsed > time_list[i]:
                compare_note = notes_list[i]
                break
        if compare_note == 0:
            shiftby = 0
        else:
            shiftby = compare_note - hz_to_midi(main_note)
        global pitchshiftby
        pitchshiftby = shiftby
        print("shift by", shiftby)
    else:
        print("OOPS")


def recorder_stream():
    with sd.Stream(samplerate=Fs, blocksize=block_size, latency="low", channels=1, callback=callback) as S:
        sd.sleep(int(duration * 1000))

    print('done')

import os
from pathlib import Path
if not os.path.isfile("tired.txt"):
    Path("tired.txt").touch()

recorder_stream()
