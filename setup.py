#!/usr/bin/env python

import os
import glob
from config import config
import pprint
from commands import getstatusoutput
import sqlite3

DIR = os.path.dirname(os.path.realpath(__file__))

rrd_filename = 'temp.rrd'
rrd_filepath = os.path.join(DIR, 'database', rrd_filename)
rrd_exists = os.path.exists(rrd_filepath)

db_filename = 'sensor_values.db'
db_filepath = os.path.join(DIR, 'database', db_filename)
db_exists = os.path.exists(db_filepath)
conn = sqlite3.connect(db_filepath)

max_display_order = 0
max_rrd_order = 0
colors = ['#66CCFF', '#0033CC', '#fdd80e', '#CC00CC', '#009900', '#CC0000', '#000000']
for sensor_id in config['temp_sensors']:
    sensor = config['temp_sensors'][sensor_id]
    if sensor['display_order'] > max_display_order:
        max_display_order = sensor['display_order']
    if sensor['rrd_order'] > max_rrd_order:
        max_rrd_order = sensor['rrd_order']
    colors.remove(sensor['color'])

modules = open('/proc/modules').read()
if 'w1_therm' not in modules:
    getstatusoutput('sudo modprobe w1-therm')
if 'w1_gpio' not in modules:
    getstatusoutput('sudo modprobe w1-gpio')

new_sensors = False
new_ds = []
new_serial = []
for file_path in glob.glob('/sys/bus/w1/devices/28-*'):
    sensor_id = os.path.basename(file_path)
    if sensor_id not in config['temp_sensors']:
        print sensor_id
        sensor_name = raw_input("Enter a name for this sensor: ")
        sensor_ds_name = sensor_name.replace(' ', '_').lower()
        alert_threshold = raw_input("Alert Threshold: ")

        if not alert_threshold:
            alert_threshold = None

        max_display_order += 1
        max_rrd_order += 1
        config['temp_sensors'][sensor_id] = {
            'name': sensor_name,
            'ds_name': sensor_ds_name,
            'alert_threshold': alert_threshold,
            'display_order': max_display_order,
            'rrd_order': max_rrd_order,
            'color': colors.pop(0)
        }
        new_sensors = True
        new_ds.append(sensor_ds_name)
        new_serial.append(sensor_id)

if new_sensors:
    if rrd_exists:
        command = 'rrdtool tune %s' % (rrd_filepath)
        for ds in new_ds:
            command += ' DS:%s:GAUGE:600:U:U' % (ds)
        status, message = getstatusoutput(command)
        if status == 0:
            print '%d new ds added to rrd' % (len(new_ds))
        else:
            print 'Error adding sensor to rrd: %s' % (message)
    if db_exists:
        cur = conn.cursor()
        for serial_code in new_serial:
            sensor = config['temp_sensors'][serial_code]
            name = sensor['name']
            cur.execute('INSERT INTO sensors \
                        (serial_code, name) \
                     VALUES \
                        (?, ?)',
                        (serial_code, name))
            conn.commit()
            print 'Added new ds to db'

    pp = pprint.PrettyPrinter(indent=4)
    f = open('config.py', 'w')
    f.write('config = %s' % pp.pformat(config))
