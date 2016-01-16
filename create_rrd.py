#!/usr/bin/env python
from config import config
import os
from commands import getstatusoutput

DIR = os.path.dirname(os.path.realpath(__file__))

temp_sensors = config['temp_sensors']
sorted_temp_sensor_ids = sorted(temp_sensors, key=lambda key: temp_sensors[key]['rrd_order'])
sorted_temp_sensors = [temp_sensors[k] for k in sorted_temp_sensor_ids]

humidity_sensors = config['humidity_sensors']
sorted_humidity_sensor_ids = sorted(humidity_sensors, key=lambda key: humidity_sensors[key]['rrd_order'])
sorted_humidity_sensors = [humidity_sensors[k] for k in sorted_humidity_sensor_ids]

databases = [
    {
        'rrd_path': os.path.join(DIR, 'temp.rrd'),
        'sensors': sorted_temp_sensors
    },
    {
        'rrd_path': os.path.join(DIR, 'humidity.rrd'),
        'sensors': sorted_humidity_sensors
    }
]

for database in databases:
    if not os.path.isfile(database['rrd_path']):
        command = 'rrdtool create %s --start N --step 300 \\\n' % (database['rrd_path'])
        for sensor in database['sensors']:
            command += 'DS:%s:GAUGE:600:U:U \\\n' % sensor['ds_name']
        command += '''RRA:AVERAGE:0.5:1:12 \\
        RRA:AVERAGE:0.5:1:288 \\
        RRA:AVERAGE:0.5:12:168 \\
        RRA:AVERAGE:0.5:12:720 \\
        RRA:AVERAGE:0.5:288:365'''
        print command
        status, message = getstatusoutput(command)
        if status == 0:
            print '%s created' % database['rrd_path']
        else:
            print 'Error creating %s' % database['rrd_path']
    else:
        print '%s already exists' % database['rrd_path']
