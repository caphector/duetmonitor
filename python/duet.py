#!/usr/bin/python3

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

def l_d(var):
    p = '\n'
    l = ', ' 
    var_name = repr(eval(variable))
    var_value = var
    var_type = type(var)
    val = 'N: {}\nV: {}\nT: {}\n'
    print_value = val.format(var_name, p, var_value, p, var_type, p)
#    print(print_value)
    return_value = val.format(var_name, l, var_value, l, var_type)
    return print_value,return_value

def get_state():
    try:
        status = requests.get(baseurl + 'rr_status?type=3')
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as e:
        pr,rv = ld(e)
        print(pr)
        duet_log(rv,'ConErr')
        time.sleep(0.5)
        pass
    duet = status.json()
    return duet, status

def get_duet(item):
    duet = get_state()[0]
    return duet[item]

def duet_logger(log_data, tag):
     log.write(datetime.datetime.now().isoformat() + ': {}: {}\n'.format(tag, log_data))

def wait_until_ready(sequence):
    before = sequence
    duet_logger(str(sequence), 'status')
    busy = { 'B', 'S', 'P' }
    while get_duet('status') in busy:
#        print('wait')
        sequence = get_duet('seq')
 #       print(sequence + get_duet('status'))
        time.sleep(0.5)
    sequence = get_duet('seq')
#    print('Sequence is {} and before is {}'.format(sequence, before))
    if sequence > before:
        reply = requests.get(baseurl + 'rr_reply')
        data = reply.text
#        print(data)
        duet_logger(data, 'status')
        if data:
            return data

def take_photo(duet):
    dir = os.environ['HOME'] + targetdir
    wait_until_ready(send_gcode(gcoder('pause')))
    log_line = 'Taking photo of ' + str(get_duet('currentLayer'))
    duet_logger(log_line, 'photo')
    wait_until_inactive()
    os.chdir(dir)
    photo = '/usr/bin/sudo /usr/bin/gphoto2 --wait-event=350ms --capture-image-and-download --filename=' + str(get_duet('currentLayer')) + '.jpg'
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

def shadow_macro(macro):
    macros = {
        lprobe = """G30 P0 X0 Y125 Z-99999
G30 P1 X108.24 Y62.5 Z-99999
G30 P2 X108.24 Y-62.5 Z-99999
G30 P3 X0 Y-125 Z-99999
G30 P4 X-108.24 Y-62.5 Z-99999
G30 P5 X-108.24 Y62.5 Z-99999
G30 P6 X0 Y62.5 Z-99999
G30 P7 X54.13 Y-31.25 Z-99999
G30 P8 X-54.13 Y-31.25 Z-99999
G30 P9 X0 Y0 Z-99999 S-1"""
        sprobe = '''G30 P0 X-87.60 Y-53.00 Z-99999	; X tower
G30 P1 X0.00 Y-102.00 Z-99999	; between X-Y towers
G30 P2 X85.60 Y-49.00 Z-99999	; Y tower
G30 P3 X82.60 Y51.00 Z-99999	; between Y-Z towers
G30 P4 X1.00 Y101.00 Z-99999	; Z tower
G30 P5 X-88.60 Y53.00 Z-99999	; between Z-X towers
G30 P6 X-43.30 Y-25.00 Z-99999	; X tower
G30 P7 X0.00 Y-50.00 Z-99999	; between X-Y towers
G30 P8 X43.30 Y-25.00 Z-99999	; Y tower
G30 P9 X43.30 Y25.00 Z-99999	; between Y-Z towers
G30 P10 X0.00 Y50.00 Z-99999	; Z tower
G30 P11 X-43.30 Y25.00 Z-99999	; between Z-X towers
G30 P12 X0 Y0 Z-99999 S-1		; center and auto-calibrate 6 factors
G1 X-87.60 Y-53.00 Z4 '''}
    return macros[macro]

def gcode_encode(line):
    code = urllib.parse.quote(line)
    return code

def probe_parse(results,macro):
    value = results
    macro_lines = macro.splitlines()
    split = value.split()
    spaces = value.count(' ')
    if spaces > 9:
            split = val.split()
            start=4
            mean = spaces - 4
            heights = spaces - 6
            Z=split[start:heights]
            probe_mean = split[mean]
            probe_dev = split[spaces]
    for item in heights:
        print("Item: {} - something".format(item))