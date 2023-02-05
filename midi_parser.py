# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:22:44 2023

@author: Alice
"""

import os
from mido import MidiFile


cv1 = MidiFile('./lyrics/Never Gonna Give You Up (Karaoke).mid', clip=True)
vocal_track_num = 11
track = []
for message in cv1.tracks[0]:
    if message.type == 'set_tempo':
        bpm = message.tempo
ticks_per_beat = cv1.ticks_per_beat
# %%
time_list = []
notes_list = []
for message in cv1.tracks[vocal_track_num]:
    if message.type == 'note_on' or message.type == 'note_off':
        time_list.append(message.time)
        notes_list.append(message.note)
        track.append(message)
import numpy as np
time_list_cum = np.cumsum(time_list)
time_list_cum = time_list_cum * (bpm/60) / ticks_per_beat
# %%
mid = MidiFile()
mid.ticks_per_beat = cv1.ticks_per_beat
mid.tracks.append(track)
mid.save(f"vocal.midi")

# %%