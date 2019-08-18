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


# @pysnooper.snoop()
def main():
    probe_dev = 2
    ready = 0.030
    send_gcode(gcoder('home'))
    warmup('pla')
#    time.sleep(300) # Wait for it to warm up
    i = 1
    log = 'Doing large radius calibration'
    log_and_print(log.format(i), 'initial_calibration')
    t1 = timer()
    while probe_dev > ready:
        log_and_print('Doing small radius calibration #{}'.format(i), 'secondary_calibration')
        start = timer()
        result = scan_result(regularprobe)
        end = timer()
        timed = (end - start)
        log_and_print('Probing took {} seconds'.format(timed), 'timer')
        cal, probe_mean, probe_dev = probe_parse(result)
        log_and_print('Completed calibration #{}. Mean: {} Dev: {}'.format(i, probe_mean, probe_dev), 'secondary_calibration')
        time.sleep(30)
    log_and_print('Calibration is under {} mean deviation after {} calibrations; ready to print after autocalibration.'.format(probe_dev, i), 'done_calibrating')
    send_gcode(gcoder('autocal'))
    t2 = timer
    time = (t2 - t1)
    log_and_print('Calibration took {} seconds'.format(time), 'timer')


main()
