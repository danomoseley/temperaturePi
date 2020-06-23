#!/usr/bin/env python3
import os
import re
import time
from config import config
from subprocess import getstatusoutput
from utils import sendAlertEmail, getExceptionInfo

DIR = os.path.dirname(os.path.realpath(__file__))

def readHumiditySensors():
    errors = []

    status, processes = getstatusoutput('ps aux')
    if not re.search("pigpiod", processes):
        getstatusoutput('sudo pigpiod')

    sensor_readings = [None]*(len(config['humidity_sensors'])+1)
    for gpio_pin, sensor in config['humidity_sensors'].items():
        failed_attempts = 0;
        readings = []
        while failed_attempts < 5:
            path = os.path.join(DIR, 'DHTXXD')
            status, output = getstatusoutput(path + ' -g' + str(gpio_pin))
            if re.match('0', output):
                humidity_re = re.search('(\d+\.\d+)$', output)
                humidity = humidity_re.group(1)
                readings.append(float(humidity))
                if len(readings) < 5:
                    time.sleep(2)
                else:
                    avg_humidity = sum(readings)/len(readings)
                    sensor_readings[sensor['rrd_order']] = avg_humidity
                    break
            else:
                failed_attempts += 1
        if failed_attempts == 5:
            errors.append('%d failed attempts at reading humidity on pin %d' % (failed_attempts, gpio_pin))

    sensor_readings = [x for x in sensor_readings if x is not None]
    if len(sensor_readings) == len(config['humidity_sensors']):
        rrd_path = os.path.join(DIR, 'database', 'humidity.rrd')
        humidity_values = ':'.join(map(str, sensor_readings))
        command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, humidity_values)
        status, message = getstatusoutput(command)
        if status != 0:
            errors.append('Error running %s - %d - %s' % (command, status, message))
    else:
        errors.append('Error processing humidity sensors')
    return errors

errors = []
try:
    sensor_errors = readHumiditySensors()
    errors.extend(sensor_errors)
except Exception as e:
    errors.append(getExceptionInfo(e))

if len(errors):
    if 'gmail' in config:
        sendAlertEmail(errors)
    print('\n'.join(errors))
