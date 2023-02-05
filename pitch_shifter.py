# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 03:26:06 2023

@author: Alice
"""

import subprocess
import pyautogui
import time
import pywinauto

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
time.sleep(1)
pyautogui.click(449, 83)  # click effects/filters
time.sleep(1)
pyautogui.click(554, 166) # click more options
time.sleep(1)
pyautogui.click(467, 166) # click advanced
time.sleep(1)
mouse_pos_x = 101 # middle of pitch shift bar
mouse_pos_y = 368


def pitch_shift(n):
    pyautogui.moveTo(mouse_pos_x, mouse_pos_y)
    pyautogui.dragTo(mouse_pos_x, mouse_pos_y - n*10, duration = 1)
    time.sleep(1)

pitch_shift(-2)
