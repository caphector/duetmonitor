#!/usr/bin/env python3

from duet import *

import json
import sys
import requests
import datetime
import urllib.parse
import time
import subprocess
import os
from os.path import expanduser
import pysnooper

ip = '192.168.1.88'
baseurl = 'http://' + ip + '/'
home = expanduser("~")
output = home + '/duetlog'
log = open(output, 'a')

#@pysnooper.snoop()
def main():
    timelapse = 'timelapse'
    layer = get_duet('currentLayer')
    seq = get_duet('seq')
    log_and_print('Starting photo for layer {} at sequence {}'.format(str(layer), str(seq)), timelapse)
    inc_layer = layer
    known = seq
    duet, status = get_state()
    while get_duet('status'):
        duet_logger(json.dumps(duet), 'json')
        layer = get_duet('currentLayer')
        seq = get_duet('seq')
        if layer > inc_layer:
#            log_and_print('Getting M122 info at layer {}'.format(str(layer)), timelapse)
            #  m122_info = wait_until_ready(send_gcode('M122'))
            #  duet_logger(m122_info, 'M122')
            take_photo(duet)
            inc_layer = get_duet('currentLayer')
            log_and_print('Took photo for layer{}'.format(str(layer)), timelapse)
        if seq > known:
            reply = requests.get(baseurl + 'rr_reply')
            duet_logger(reply.text, 'reply')
            known = seq
        time.sleep(0.300)

main()
