#!/usr/bin/env python3

from duet import wait_until_ready, send_gcode
import os


ip = '192.168.1.88'
baseurl = 'http://' + ip + '/'
output = '~/duetlog'
log = open(output, 'a')
targetdir = '/timelapse'

targetdir = os.environ['HOME'] + targetdir


def main():
    wait_until_ready(send_gcode('M122'))

main()
