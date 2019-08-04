#!/usr/bin/python3

from duet import *

import os
import json
import sys
import requests
import datetime
import urllib.parse
import time
import subprocess

ip = '192.168.1.72'
baseurl='http://' + ip + '/'
output = '/tmp/file'
log = open(output, 'a')
targetdir = '/timelapse'

targetdir= os.environ['HOME'] + targetdir

largeprobe = 'M98 P/macros/py/snoprobe.g'

regularprobe = 'M98 P/macros/py/probe.g'

autocalibration = 'G32'

retract = ''
extrude = ''

lprobe = """G30 P0 X0 Y125 Z-99999
G30 P1 X108.24 Y62.5 Z-99999
G30 P2 X108.24 Y-62.5 Z-99999
G30 P3 X0 Y-125 Z-99999
G30 P4 X-108.24 Y-62.5 Z-99999
G30 P5 X-108.24 Y62.5 Z-99999
G30 P6 X0 Y62.5 Z-99999
G30 P7 X54.13 Y-31.25 Z-99999
G30 P8 X-54.13 Y-31.25 Z-99999
G30 P9 X0 Y0 Z-99999 S-1"""

sprobe = '''G30 P0 X-87.60 Y-53.00 Z-99999	; X tower
G30 P1 X0.00 Y-102.00 Z-99999	; between X-Y towers
G30 P2 X85.60 Y-49.00 Z-99999	; Y tower
G30 P3 X82.60 Y51.00 Z-99999	; between Y-Z towers
G30 P4 X1.00 Y101.00 Z-99999	; Z tower
G30 P5 X-88.60 Y53.00 Z-99999	; between Z-X towers
G30 P6 X-43.30 Y-25.00 Z-99999	; X tower
G30 P7 X0.00 Y-50.00 Z-99999	; between X-Y towers
G30 P8 X43.30 Y-25.00 Z-99999	; Y tower
G30 P9 X43.30 Y25.00 Z-99999	; between Y-Z towers
G30 P10 X0.00 Y50.00 Z-99999	; Z tower
G30 P11 X-43.30 Y25.00 Z-99999	; between Z-X towers
G30 P12 X0 Y0 Z-99999 S-1		; center and auto-calibrate 6 factors
G1 X-87.60 Y-53.00 Z4 '''

def scan_result(gcode):
    result = wait_until_ready(send_gcode(gcode))
    return result

def run_scan():
#    send_gcode(gcoder('less probe'))
    warmup=scan_result(largeprobe)
    print(warmup)
#    wait_until_ready(send_gcode(regularprobe))
#    wait_until_ready(send_gcode(regularprobe))
#    wait_until_ready(send_gcode(autocalibration))

run_scan()