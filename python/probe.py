#!/usr/bin/python3

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
output = '/tmp/file'
log = open(output, 'a')
targetdir = '/timelapse'

targetdir= os.environ['HOME'] + targetdir

largeprobe = 'M98 P/macros/py/snoprobe.g'

regularprobe = 'M98 P/macros/py/probe.g'

autocalibration = 'G32'

def scan_result(gcode):
    result = wait_until_ready(send_gcode(gcode))
    return result

def main():
    send_gcode(gcoder('home'))
    warmup('pla')
#    time.sleep(300) # Wait for it to warm up
#    for scan in (largeprobe, largeprobe, regularprobe, regularprobe, autocalibration):
    for scan in (largeprobe, largeprobe):
        result = scan_result(scan)
        log_and_print(result, 'scan')
        probe_parse(result)

main()

