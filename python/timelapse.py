#!/usr/bin/python3

from duet import *

import json
import sys
import requests
import datetime
import urllib.parse
import time
import subprocess
import os


ip = '192.168.1.72'
baseurl = 'http://' + ip + '/'
output = '/tmp/file'
log = open(output, 'a')
targetdir = '/timelapse'

def main():
    print('starting')
    layer = get_duet('currentLayer')
    seq = get_duet('seq')
    inc_layer = layer
    known = seq
    duet, status = get_state()
    while get_duet('status'):
        duet_logger(json.dumps(duet), 'json')
        layer = get_duet('currentLayer')
        seq = get_duet('seq')
        print(seq)
        print('photo')
        if layer > inc_layer:
            take_photo(duet)
            inc_layer = get_duet('currentLayer')
        if seq > known:
            reply = requests.get(baseurl + 'rr_reply')
            duet_logger(reply.text, 'reply')
            known = seq
        time.sleep(0.300)

main()
