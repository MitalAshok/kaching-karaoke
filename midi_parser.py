# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:22:44 2023

@author: Alice
"""

from mido import MidiFile

cv1 = MidiFile('./lyrics/Never Gonna Give You Up (Karaoke).mid')
#cv1 = MidiFile('./lyrics/Never_Gonna_Give_You_Up_Flute.mid', clip=True)
vocal_track_num = 11
track = []
for message in cv1.tracks[0]:
    if message.type == 'set_tempo':
        usperbeat = message.tempo
ticks_per_beat = cv1.ticks_per_beat


time_list = []
notes_list = []
for message in cv1.tracks[vocal_track_num]:
    if message.type == 'note_on' or message.type == 'note_off':
        time_list.append(message.time)
        notes_list.append(message.note)
        track.append(message)
import numpy as np
time_list_cum = np.cumsum(time_list)
time_list_cum = time_list_cum * (usperbeat / ticks_per_beat) / 1e6

# %%
time_list = []
notes_list = []
cum_time = 0
for message in cv1.tracks[vocal_track_num]:
    cum_time += message.time
    if message.type == 'note_on':
        time_list.append(cum_time)
        cum_time = 0
        notes_list.append(message.note)
        track.append(message)

time_list = [time * (usperbeat / ticks_per_beat) / 1e6 for time in time_list]
import numpy as np
time_list[0] == 18800
time_list = np.cumsum(time_list)


# %%
'''
import mido
import recorder
port = mido.open_output('Microsoft GS Wavetable Synth 0')
mid = mido.MidiFile('./lyrics/Never Gonna Give You Up (Karaoke).mid')
for msg in mid.play():
    port.send(msg)
    if msg.channel==11:
        try:
            sd.Stream(samplerate=Fs, blocksize=block_size, latency="low", channels=1, callback=callback) as S:
                sd.sleep(msg.time *
            print(msg)
        except:
            print(msg)
'''