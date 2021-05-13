#!/usr/bin/env python3
from config import config
import os
from subprocess import getstatusoutput

DIR = os.path.dirname(os.path.realpath(__file__))

remote_path = os.path.join(config['remote']['path'], 'database')

command = "rsync -a --bwlimit=500 %s/database/ %s@%s:%s" % (DIR, config['remote']['user'], \
    config['remote']['host'], remote_path)
status, message = getstatusoutput(command)
if status != 0:
    print(message)

command = "rsync -a --bwlimit=500 %s/config.py %s@%s:%s" % (DIR, config['remote']['user'], \
    config['remote']['host'], config['remote']['path'])
status, message = getstatusoutput(command)
if status != 0:
    print(message)
