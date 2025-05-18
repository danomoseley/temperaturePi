#!/usr/bin/env python3
from config import config
import os
from subprocess import getstatusoutput

DIR = os.path.dirname(os.path.realpath(__file__))

temp_sensors = config['temp_sensors']
sorted_temp_sensor_ids = sorted(temp_sensors, key=lambda key: temp_sensors[key]['rrd_order'])
sorted_temp_sensors = [temp_sensors[k] for k in sorted_temp_sensor_ids]

humidity_sensors = config['humidity_sensors']
sorted_humidity_sensor_ids = sorted(humidity_sensors, key=lambda key: humidity_sensors[key]['rrd_order'])
sorted_humidity_sensors = [humidity_sensors[k] for k in sorted_humidity_sensor_ids]

lake_temp_sensors = config['lake_temp_sensors']
sorted_lake_temp_sensor_ids = sorted(lake_temp_sensors, key=lambda key: lake_temp_sensors[key]['rrd_order'])
sorted_lake_temp_sensors = [lake_temp_sensors[k] for k in sorted_lake_temp_sensor_ids]

pressure_sensors = config['pressure_sensors']
sorted_pressure_sensor_ids = sorted(pressure_sensors, key=lambda key: pressure_sensors[key]['rrd_order'])
sorted_pressure_sensors = [pressure_sensors[k] for k in sorted_pressure_sensor_ids]

wind_speed_sensors = config['wind_speed_sensors']
sorted_wind_speed_sensor_ids = sorted(wind_speed_sensors, key=lambda key: wind_speed_sensors[key]['rrd_order'])
sorted_wind_speed_sensors = [wind_speed_sensors[k] for k in sorted_wind_speed_sensor_ids]

radon_sensors = config['radon_sensors']
sorted_radon_sensor_ids = sorted(radon_sensors, key=lambda key: radon_sensors[key]['rrd_order'])
sorted_radon_sensors = [radon_sensors[k] for k in sorted_radon_sensor_ids]

directory = os.path.join(DIR, 'database')

if not os.path.exists(directory):
    os.makedirs(directory)

databases = [
    {
        'rrd_path': os.path.join(directory, 'temp.rrd'),
        'sensors': sorted_temp_sensors
    },
    {
        'rrd_path': os.path.join(directory, 'humidity.rrd'),
        'sensors': sorted_humidity_sensors
    },
    {
        'rrd_path': os.path.join(directory, 'lake_temp.rrd'),
        'sensors': sorted_lake_temp_sensors
    },
    {
        'rrd_path': os.path.join(directory, 'pressure.rrd'),
        'sensors': sorted_pressure_sensors
    },
    {
        'rrd_path': os.path.join(directory, 'pressure_hpa.rrd'),
        'sensors': sorted_pressure_sensors
    },
    {
        'rrd_path': os.path.join(directory, 'wind_speed.rrd'),
        'sensors': sorted_wind_speed_sensors
    },
    {
        'rrd_path': os.path.join(directory, 'radon.rrd'),
        'sensors': sorted_radon_sensors
    },
]

for database in databases:
    if not os.path.isfile(database['rrd_path']) and len(database['sensors']):
        command = 'rrdtool create %s --start N --step 300 \\\n' % (database['rrd_path'])
        for sensor in database['sensors']:
            command += 'DS:%s:GAUGE:600:U:U \\\n' % sensor['ds_name']
        command += '''RRA:AVERAGE:0.5:1:12 \\
        RRA:AVERAGE:0.5:1:288 \\
        RRA:AVERAGE:0.5:12:168 \\
        RRA:AVERAGE:0.5:12:720 \\
        RRA:AVERAGE:0.5:288:365'''
        status, message = getstatusoutput(command)
        if status == 0:
            print('%s created' % database['rrd_path'])
        else:
            print('Error creating %s - %s' % (database['rrd_path'], message))
    else:
        print('%s already exists' % database['rrd_path'])
