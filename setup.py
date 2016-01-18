#!/usr/bin/env python

import os
import glob
from config import config
import pprint

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
for file_path in glob.glob('/sys/bus/w1/devices/28-*'):
    sensor_id = os.path.basename(file_path)
    if sensor_id not in config['temp_sensors']:
        print sensor_id
        sensor_name = raw_input("Enter a name for this sensor: ")
        alert_threshold = raw_input("Alert Threshold: ")

        if not alert_threshold:
            alert_threshold = None

        max_display_order += 1
        max_rrd_order += 1
        config['temp_sensors'][sensor_id] = {
            'name': sensor_name,
            'ds_name': sensor_name.replace(' ', '_').lower(),
            'alert_threshold': alert_threshold,
            'display_order': max_display_order,
            'rrd_order': max_rrd_order,
            'color': colors.pop(0)
        }
        new_sensors = True

if new_sensors:
    pp = pprint.PrettyPrinter(indent=4)
    f = open('config.py', 'w')
    f.write('config = %s' % pp.pformat(config))
