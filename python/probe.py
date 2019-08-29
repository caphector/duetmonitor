#!/usr/bin/env python3

import duet as du

import logging
import os
import time
from os.path import expanduser
import pysnooper
from timeit import default_timer as timer
import logging

ip = '192.168.1.88'
baseurl = 'http://' + ip + '/'
home = expanduser("~")
output = home + '/duetlog'
log = open(output, 'a')
targetdir = '/timelapse'

targetdir = os.environ['HOME'] + targetdir

probe = 'M98 P/macros/py/probe.g'
autocalibration = 'G32'

logger = logging.getLogger('duet-log')


def scan_result(gcode):
    result = du.wait_until_ready(du.send_gcode(gcode))
    return result


logger = logging.getLogger('duet-log')


#@pysnooper.snoop()
def main():
    probe_dev = 2
    ready = 0.030
#    du.send_gcode(du.gcoder('home'))
#    du.warmup('pla')
#    time.sleep(300) # Wait for it to warm up
    waitforit = 1
    i = 1
    log = 'Performing calibration'
    logger.info(log.format(i))
    t1 = timer()
    while waitforit < 2:
        logger.info('Calibration run #{}'.format(i))
        start = timer()
        if i > 1:
            logger.debug('30 seconds to cancel')
            time.sleep(30)
        result = scan_result(probe)
        end = timer()
        timed = (end - start)
        cal, probe_mean, probe_dev = du.probe_parse(result)
        logger.info('Completed calibration #{}. Mean: {} Dev: {} in {:.0f}s'.format(i, probe_mean, probe_dev, timed))
        if probe_dev < ready:
            waitforit += 1
    du.send_gcode(du.gcoder('autocal'))
    t2 = timer
    calibration_time = (t2 - t1)
    logger.info('Calibration under {} deviation after {} calibrations; assuming printer is warmed up after {:.0f}s.'.format(probe_dev, i, calibration_time))


main()
