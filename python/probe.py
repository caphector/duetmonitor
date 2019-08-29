#!/usr/bin/env python3

import duet as du

import logging
import os
import time
from os.path import expanduser
# import pysnooper
from timeit import default_timer as timer
import logging

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

logger = logging.getLogger('duet-log')


def scan_result(gcode):
    result = du.wait_until_ready(du.send_gcode(gcode))
    return result


logger = logging.getLogger('duet-log')


# @pysnooper.snoop()
def main():
    probe_dev = 2
    ready = 0.030
    du.send_gcode(du.gcoder('home'))
#    du.warmup('pla')
#    time.sleep(300) # Wait for it to warm up
    i = 1
    log = 'Doing large radius calibration'
    du.log_and_print(log.format(i), 'initial_calibration')
    t1 = timer()
    while probe_dev > ready:
        logger.info('Doing small radius calibration #{}'.format(i))
        start = timer()
        result = scan_result(regularprobe)
        end = timer()
        timed = (end - start)
        cal, probe_mean, probe_dev = du.probe_parse(result)
        logger.info('Completed calibration #{}. Mean: {} Dev: {} in {}'.format(i, probe_mean, probe_dev, timed))
        time.sleep(30)
    du.log_and_print('Calibration is under {} mean deviation after {} calibrations; ready to print after autocalibration.'.format(probe_dev, i), 'done_calibrating')
    du.send_gcode(du.gcoder('autocal'))
    t2 = timer
    calibration_time = (t2 - t1)
    logging.info('Calibration took {} seconds'.format(calibration_time), 'timer')


main()
