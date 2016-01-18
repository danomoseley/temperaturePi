#!/usr/bin/python
import paramiko
import os
from commands import getstatusoutput
from config import config

DIR = os.path.dirname(os.path.realpath(__file__))

if os.path.isfile(os.path.join(DIR, 'database', 'temp.rrd')):
    getstatusoutput(os.path.join(DIR, 'get_temp.py'))

if os.path.isfile(os.path.join(DIR, 'database', 'humidity.rrd')):
    getstatusoutput(os.path.join(DIR, 'get_humidity.py'))

getstatusoutput(os.path.join(DIR, 'create_graphs.py'))

remote_path = os.path.join(config['remote']['path'], 'latest_graphs')

command = "rsync -a --bwlimit=500 %s/latest_graphs/ %s@%s:%s" % (DIR, config['remote']['user'], \
    config['remote']['host'], remote_path)

status, message = getstatusoutput(command)

if status != 0:
    print message
