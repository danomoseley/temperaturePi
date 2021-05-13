#!/usr/bin/python3
import os
from subprocess import getstatusoutput
from config import config
from datetime import datetime, timedelta
import get_temp
import get_lake_temp
import get_pressure
import get_humidity
import create_graphs

DIR = os.path.dirname(os.path.realpath(__file__))

if os.path.isfile(os.path.join(DIR, 'database', 'temp.rrd')):
    get_temp.process()

if os.path.isfile(os.path.join(DIR, 'database', 'humidity.rrd')):
    get_humidity.process()

if os.path.isfile(os.path.join(DIR, 'database', 'pressure.rrd')):
    get_pressure.process()

if os.path.isfile(os.path.join(DIR, 'database', 'lake_temp.rrd')):
    get_lake_temp.process()

create_graphs.createGraphs()

expires = datetime.utcnow() + timedelta(minutes=5)

s3_path = config['s3']
command = "/usr/local/bin/aws s3 cp --recursive --quiet %s/latest_graphs/ %s/latest_graphs/ --expires '%s'" % (DIR, s3_path, expires.isoformat())

status, message = getstatusoutput(command)

if status != 0:
    print(message)

