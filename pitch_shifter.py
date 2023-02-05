# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 03:26:06 2023

@author: Alice
"""

import subprocess
import pyautogui
import time
import pywinauto
from globalstate import pitchshifter_ready
import os

def start_pitchshifter():
    print("should open")
    subprocess.Popen([r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
                      "./lyrics/Rick Astley - Never Gonna Give You Up (Official Music Video).wav",
                      ])

    import win32gui, win32con

    def winEnumHandler( hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
            if 'VLC' in win32gui.GetWindowText(hwnd):
               win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
               return

    win32gui.EnumWindows( winEnumHandler, None )
    time.sleep(2)

    #pyautogui.hotkey("ctrlleft", "E")
    pyautogui.click(381, 48)  # click tools
    time.sleep(0.5)
    pyautogui.click(449, 83)  # click effects/filters
    time.sleep(0.5)
    pyautogui.click(554, 166) # click more options
    time.sleep(0.5)
    pyautogui.click(467, 166) # click advanced
    time.sleep(0.5)

    global pitchshifter_ready
    pitchshifter_ready = True
    print("SET PITCH SHIFTER TO READY!")


def pitch_shift(n):
    mouse_pos_x = 101 # middle of pitch shift bar
    mouse_pos_y = 368
    pyautogui.moveTo(mouse_pos_x, mouse_pos_y)
    pyautogui.dragTo(mouse_pos_x, mouse_pos_y - n*10, duration = 0.5)

if __name__ == "__main__":


    while not os.path.isfile("tired.txt"):
        time.sleep(0.1)
    start_pitchshifter()
    #pitch_shift(-2)
    #pitch_shift(5)
