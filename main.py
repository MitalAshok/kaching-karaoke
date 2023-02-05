# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 07:08:49 2023

@author: Alice
"""
import subprocess

if __name__ == '__main__':
    subprocess.call("python pitch_shifter.py", shell=True)
    subprocess.call("python recorder.py", shell=True)