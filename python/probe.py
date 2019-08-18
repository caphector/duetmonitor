#!/usr/bin/env python3

from duet import *


import os
import json
import sys
import datetime
import urllib.parse
import time
import subprocess
from os.path import expanduser
import pysnooper
from timeit import default_timer as timer

ip = '192.168.1.88'
baseurl = 'http://' + ip + '/'
home = expanduser("~")
output = home + '/duetlog'
log = open(output, 'a')
targetdir = '/timelapse'

targetdir = os.environ['HOME'] + targetdir

largeprobe = 'M98 P/macros/py/snoprobe.g'
regularprobe = 'M98 P/macros/py/probe.g'
autocalibration = 'G32'


def scan_result(gcode):
    result = wait_until_ready(send_gcode(gcode))
    return result


@pysnooper.snoop()
def main():
    probe_dev = 2
    initial = 0.100
    ready = 0.020
    send_gcode(gcoder('home'))
    warmup('pla')
#    time.sleep(300) # Wait for it to warm up
    i = 1
    log = 'Doing large radius calibration'
    log_and_print(log.format(i), 'initial_calibration')

    while probe_dev > initial:
        start = timer()
        result = scan_result(regularprobe)
        end = timer()
        log_and_print(end - start, 'timer')
        print(result)
        cal, probe_mean, probe_dev = probe_parse(result)
        log = 'Completed large radius calibration #{}. Mean: {} Dev: {}'
        log_and_print(log.format(i, probe_mean, probe_dev), 'initial_calibration')
        time.sleep(30)
    log_and_print('Calibration is under {} mean deviation after {} calibrations; ready to print after autocalibration.'.format(probe_dev, i), 'done_calibrating')
    send_gcode(gcoder('autocal'))

main()
