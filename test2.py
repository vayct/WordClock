#!/usr/bin/python


import sys, os, time, argparse, atexit, signal, random
from datetime import datetime
from string import digits
from rgbmatrix import Adafruit_RGBmatrix

# Constants
MATRIX_W      = 32 # Number of Actual X Pixels
MATRIX_H      = 32 # Number of Actual Y Pixels
MATRIX_DEPTH  = 3  # Color Depth (RGB=3)
MATRIX_DIV    = 2  # Physical Matrix is Half of Pixel Matrix

# Enumerate RGB Matrix Object
matrix = Adafruit_RGBmatrix(MATRIX_H, MATRIX_W/MATRIX_H)

def exit_handler():
	print 'Scripted Aborted'
	matrix.Clear()

atexit.register(exit_handler)
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))


fb = [0] * MATRIX_W * MATRIX_H * MATRIX_DEPTH



for i in range(3072):
	if i % 3 == 2:
		fb[i] = 55
	if i % 3 == 1:
		fb[i] = 66
#3072
matrix.SetBuffer(fb)
time.sleep(100)

print len(fb)  




