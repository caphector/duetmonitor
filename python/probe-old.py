#!/usr/bin/python3

import os
import json
import sys
import requests
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

retract = ''
extrude = ''

def get_state():
    status = requests.get(baseurl + 'rr_status?type=3')
    duet = status.json()
    return duet,status

def get_duet(item):
    duet = get_state()[0]
    return duet[item]

def duet_logger(log_data, tag):
     log.write(datetime.datetime.now().isoformat() + ': {}: {}\n'.format(tag, log_data))

def wait_until_ready(sequence):
    print(get_duet('status'))
    print(get_duet('seq'))
    before = sequence
    duet_logger(get_duet('status'), 'status')
    duet_logger(str(sequence), 'status')
    busy = { 'B', 'S', 'P' }
    while get_duet('status') in busy:
#        print('wait')
        sequence = get_duet('seq')
 #       print(sequence + get_duet('status'))
        time.sleep(0.5)
    time.sleep(0.25)
    sequence = get_duet('seq')
    print(sequence)
    time.sleep(0.25)
    sequence = get_duet('seq')
    print(sequence)
    if sequence > before:
        reply = requests.get(baseurl + 'rr_reply')
        data = reply.text
        print(data)
        duet_logger(data, 'status')
        if data:
            return data

def take_photo(duet):
    dir = os.environ['HOME'] + targetdir
    send_gcode(gcoder('pause'))
    log_line = 'Taking photo of ' + str(get_duet('currentLayer'))
    duet_logger(log_line, 'photo')
    wait_until_inactive()
    os.chdir(dir)
    photo = '/usr/bin/sudo /usr/bin/gphoto2 --wait-event=300ms --capture-image-and-download --filename=' + str(get_duet('currentLayer')) + '.jpg'
#    print(photo)
    subprocess.run(photo.split(), stdout=subprocess.DEVNULL)
    send_gcode(gcoder('resume'))
    
def send_gcode(code):
    code = urllib.parse.quote(code)
    url = baseurl + 'rr_gcode?gcode=' + code
    sequence = get_duet('seq')
    good = requests.get(url)
    return sequence

def gcoder(word):
    gcodes = {
        "pause":"M226",
        "resume":"M24",
        "more_probe":"M558 P4 H3 I1 R1 A4 B1",
        "less_probe":"M558 P4 H3 I1 R1 A1 B1",
        "home":"G28",
        "autocal":"G32",
        "probe":"G30 P" # Probe syntax G30 P# X# Y# Z-99999 to P9 And sned S-1
    }
    return gcodes[word]

def gcode_encode(line):
    code = urllib.parse.quote(line)
    return code

def run_scan(gcode):
#    send_gcode(gcoder('less probe'))
    print(gcode)
    wait_until_ready(send_gcode(largeprobe))
    wait_until_ready(send_gcode(regularprobe))
    wait_until_ready(send_gcode(regularprobe))
    wait_until_ready_until_ready(send_gcode(autocalibration))
    