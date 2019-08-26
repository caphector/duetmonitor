#!/usr/bin/env python3

import duet as du

import json
import requests
import time
from os.path import expanduser
import logging
import pysnooper

ip = '192.168.1.88'
baseurl = 'http://' + ip + '/'
home = expanduser("~")
output = home + '/duetlog'
log = open(output, 'a')


logger = logging.getLogger('duet-log')

@pysnooper.snoop()
def main():
    layer = du.get_duet('currentLayer')
    seq = du.get_duet('seq')
    logger.info('Starting photo for layer {} at sequence {}'.format(str(layer), str(seq)), 'timelapse')
    inc_layer = layer
    known = seq
    duet, status = du.get_state()
    while du.get_duet('status'):
        logger.debug(json.dumps(duet))
        layer = du.get_duet('currentLayer')
        seq = du.get_duet('seq')
        if layer > inc_layer:
            logger.info('Layer changed to {}. Starting take_photo. Seq {}'.format(layer, seq))
            du.take_photo(duet)
            inc_layer = du.get_duet('currentLayer')
            logger.debug('Took photo for layer{}'.format(str(layer)))
        if seq > known:
            reply = requests.get(baseurl + 'rr_reply')
            logger.info(reply.text, 'reply')
            known = seq
        time.sleep(0.300)


main()
