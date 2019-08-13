#!/usr/bin/env python3

from duet import *

import os
import json
import sys
import datetime
import urllib.parse
import time
import subprocess

ip = '192.168.1.72'
baseurl='http://' + ip + '/'
output = '~/duetlog'
log = open(output, 'a')
targetdir = '/timelapse'

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

results = 'G32 bed probe heights: 0.018 0.014 -0.181 -0.399 -0.008 -0.146 -0.189 -0.102 -0.114 -0.162, mean -0.127, deviation from mean 0.118'
#results = 'G32 bed probe heights: -0.008 -0.073 0.075 -0.203 0.038 -0.025 -0.010 0.027 0.033 0.005 -0.007 -0.046 -0.033, mean -0.017, deviation from mean 0.065'

largeprobe = 'M98 P/macros/py/snoprobe.g'
regularprobe = 'M98 P/macros/py/probe.g'
autocalibration = 'G32'

scans =

def scan_result(gcode):
    cal, probe_mean, probe_dev = wait_until_ready(send_gcode(gcode))
    return cal, probe_mean, probe_dev

def main():
    probe_dev = 2
    initial = 0.1
    ready = 0.030
    send_gcode(gcoder('home'))
    warmup('pla')
#    time.sleep(300) # Wait for it to warm up
#    for scan in (largeprobe, largeprobe, regularprobe, regularprobe, autocalibration):
    i = 0
    while probe_dev > initial:
        cal, probe_mean, probe_dev = scan_result(largescan)
        time.sleep(0.1)
        while probe_dev > warmup:
            cal, probe_mean, probe_dev = scan_result(regularprobe)
            time.sleep(0.1)
#    for scan in (largeprobe, largeprobe):
#        result = scan_result(scan)
#        log_and_print(result, 'scan')
#        cal, probe_mean, probe_dev = probe_parse(result)
