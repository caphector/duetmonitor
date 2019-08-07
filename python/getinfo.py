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
output = '/tmp/file'
log = open(output, 'a')
targetdir = '/timelapse'

targetdir= os.environ['HOME'] + targetdir

def main():
    wait_until_ready(send_gcode('M122'))


main()

