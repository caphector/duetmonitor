#!/usr/bin/env python3

import json
import sys
import requests
import datetime
import urllib
import time
import subprocess
import os
from os.path import expanduser
import pysnooper

###
#
# ToDo: Add probing macro generation
# Add file interaction on Duet (read/write)
# Calibrate then print
# Slice while calibrating and then print
# ??? Something computer vision ???
#

ip = '192.168.1.88'
baseurl = 'http://' + ip + '/'
targetdir = '/timelapse'
home = expanduser("~")
output = home + '/duetlog'
log = open(output, 'a')


def log_and_print(data, reason):
    print(data, reason)
    duet_logger(data, reason)


def l_d(var):
    p = '\n'
    l = ', '
    var_value = var
    var_type = type(var)
    val = 'V: {}\nT: {}\n'
    print_value = val.format(var_value, p, var_type, p)
    return_value = val.format(var_value, l, var_type)
    return print_value, return_value

def get_state():
    try:
        status = requests.get(baseurl + 'rr_status?type=3')
    except Exception as e:
#        pr = l_d(e)
#       print(pr)
        log_and_print(e, 'ConErr')
        time.sleep(0.5)
        pass
    except KeyboardInterrupt:
        exit(1)
    duet = status.json()
#    print('Duet is: {}\nStatus is: {}'.format(duet, status))
    return duet, status


def get_duet(item):
    duet = get_state()[0]
#    string = 'Field: {}\n Value: {}'.format(item, duet[item])
#    log_and_print(string, 'get_duet result')
    return duet[item]


def duet_logger(log_data, tag):
    log.write(datetime.datetime.now().isoformat() + ': {}: {}\n'.format(tag, log_data))

#@pysnooper.snoop()
def wait_until_ready(sequence):
    function = 'wait_until_ready'
    before = sequence
#    log_and_print(str(sequence), function)
    busy = {'B', 'P'}
    while get_duet('status') in busy:
        time.sleep(.5)
    time.sleep(10)
    sequence = get_duet('seq')
    message = 'Sequence is now {} and was {}'.format(sequence, before)
    log_and_print(message, function)
    if sequence > before:
        reply = requests.get(baseurl + 'rr_reply')
        data = reply.text
        log_and_print(data, function)
        if data:
            return data

#@pysnooper.snoop()
def take_photo(duet):  # Compile timelapse: avconv -y -r 25 -i Prusa-%d.jpg -r 25 -vcodec copy -crf 20 -g 6 compiled.mp4
    function = 'take_photo'
    dir = os.environ['HOME'] + targetdir
    log_and_print('pausing', function)
    wait_until_ready(send_gcode(gcoder('pause')))
    log_line = 'Sent pause and taking photo of '
    log_and_print(log_line + str(get_duet('currentLayer')), function)
    os.chdir(dir)
    image = ' --filename=' + str(get_duet('currentLayer')) + '.jpg'
    photo = '/usr/bin/sudo /usr/bin/gphoto2 --wait-event=350ms --capture-image-and-download'
    log_and_print(photo, function)
    command = (photo + image)
    subprocess.run(command, stdout=subprocess.DEVNULL, shell=True)
    send_gcode(gcoder('resume'))


def send_gcode(code):
    code = gcode_encode(code)
    url = baseurl + 'rr_gcode?gcode=' + code
    sequence = get_duet('seq')
    requests.get(url)
    return sequence


def gcoder(word):
    gcodes = {
        "pause": "M226",
        "resume": "M24",
        "more_probe": "M558 P4 H3 I1 R1 A4 B1",
        "less_probe": "M558 P4 H3 I1 R1 A1 B1",
        "home": "G28",
        "autocal": "G32",
        "probe": "G30 P" # Probe syntax G30 P# X# Y# Z-99999 to P9 And sned S-1
    }
    return gcodes[word]


def shadow_macro(macro):
    macros = {
        "lprobe": """G30 P0 X0 Y125 Z-99999
G30 P1 X108.24 Y62.5 Z-99999
G30 P2 X108.24 Y-62.5 Z-99999
G30 P3 X0 Y-125 Z-99999
G30 P4 X-108.24 Y-62.5 Z-99999
G30 P5 X-108.24 Y62.5 Z-99999
G30 P6 X0 Y62.5 Z-99999
G30 P7 X54.13 Y-31.25 Z-99999
G30 P8 X-54.13 Y-31.25 Z-99999
G30 P9 X0 Y0 Z-99999 S-1""",
        "sprobe": '''G30 P0 X-87.60 Y-53.00 Z-99999	; X tower
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
G1 X-87.60 Y-53.00 Z4 '''
    }
    return macros[macro]


def gcode_encode(line):
    code = urllib.parse.quote(line)
    return code


def warmup(material):
    bed = 55
    extruder = 195
    bed = "M190 {}".format(str(bed))
    extruder = "M109 {}".format(str(extruder))
    print('Bed "{}", Extruder "{}"'.format(bed, extruder))
#    send_gcode(bed)
#    send_gcode(extruder)
    return


# def material():
#     materials = {
#       'pla': {'extruder': 195. 'bed': 55}
#         'petg': {'extruder': 225. 'bed': 90} }
#     return material[materials]


def probe_parse(results):
    spaces = results.count(' ')
    results = results.replace(',', '')
#    coord_order = 'Xcoord, Ycoord, Zcoord'  # Coord format - match here - G
    if spaces == 22:  # 30 P4 X-108.24 Y-62.5 Z-99999
        macro = shadow_macro('sprobe')
    elif spaces == 19:
        macro = shadow_macro('lprobe')
    else:
        return None, None, None
    split = results.split()
    Zcoords = split[4:-7]
    Zcoords = list(map(float, Zcoords))
    probe_mean = float(split[-5])
    probe_dev = float(split[-1])
#    log_and_print(coord_order, 'parse-coords-xyz')
    Xcoords, Ycoords = parse_macro(macro)
    cal = zip(Xcoords, Ycoords, Zcoords)
    #    for line in list(cal):
    #        log_and_print(line, 'parse-coords-xyz')
    #    data = "Z: {}, Mean: {}, Deviation: {}".format(Zcoords, probe_mean, probe_dev)
    return cal, probe_mean, probe_dev


def parse_macro(macro):
    macro_lines = macro.split('\n')
    Xcoords, Ycoords = list(), list()
    for line in macro_lines:         # G30 P4 X-108.24 Y-62.5 Z-99999
        split = line.split()
        Xcoord, Ycoord = split[2][1:], split[3][1:]
        Xcoords.append(float(Xcoord))
        Ycoords.append(float(Ycoord))
    return Xcoords, Ycoords
