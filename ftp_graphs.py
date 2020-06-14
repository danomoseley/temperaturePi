#!/usr/bin/python3
import os
from subprocess import getstatusoutput
from config import config
from datetime import datetime, timedelta

DIR = os.path.dirname(os.path.realpath(__file__))

if os.path.isfile(os.path.join(DIR, 'database', 'temp.rrd')):
    getstatusoutput(os.path.join(DIR, 'get_temp.py'))

if os.path.isfile(os.path.join(DIR, 'database', 'humidity.rrd')):
    getstatusoutput(os.path.join(DIR, 'get_humidity.py'))

if os.path.isfile(os.path.join(DIR, 'database', 'lake_temp.rrd')):
    getstatusoutput(os.path.join(DIR, 'get_lake_temp.py'))

getstatusoutput(os.path.join(DIR, 'create_graphs.py'))

expires = datetime.utcnow() + timedelta(minutes=5)

s3_path = config['s3']
command = "/usr/local/bin/aws s3 cp --recursive --quiet %s/latest_graphs/ %s/latest_graphs/ --expires '%s'" % (DIR, s3_path, expires.isoformat())

status, message = getstatusoutput(command)

if status != 0:
    print(message)

