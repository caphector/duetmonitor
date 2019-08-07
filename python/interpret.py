#!/usr/bin/env python3

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
baseurl = 'http://' + ip + '/'
output = '/tmp/file'
log = open(output, 'a')
targetdir = '/timelapse'

targetdiR = os.environ['HOME'] + targetdir

largeprobe = 'M98 P/macros/py/snoprobe.g'

regularprobe = 'M98 P/macros/py/probe.g'

autocalibration = 'G32'

file = '/Users/duncan/python/duetmonitor/python/gtest.txt'


def get_output():
    with open(file) as fp:
        line = fp.readlines()
    return line


for line in get_output():
    print(line)
    probe_parse(line)
