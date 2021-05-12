#!/usr/bin/env python3
import os
import re
import time
from config import config
from subprocess import getstatusoutput
from utils import sendAlertEmail, getExceptionInfo
import board
import busio
import adafruit_bmp280
from utils import convert_c_to_f

DIR = os.path.dirname(os.path.realpath(__file__))

def readPressureSensors():
    errors = []
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    rrd_path = os.path.join(DIR, 'database', 'pressure.rrd')
    pressure_hpa = sensor.pressure
    pressure_inhg = pressure_hpa / 33.86389
    command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, pressure_inhg)
    status, message = getstatusoutput(command)
    if status != 0:
        errors.append('Error running %s - %d - %s' % (command, status, message))

    rrd_path = os.path.join(DIR, 'database', 'pressure_hpa.rrd')
    command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, pressure_hpa)
    status, message = getstatusoutput(command)
    if status != 0:
        errors.append('Error running %s - %d - %s' % (command, status, message))
   

    #print("\nTemperature: %0.1f F" % convert_c_to_f(sensor.temperature))
    #print("Pressure: %0.1f hPa" % pressure_hpa)
    #print("Pressure: %0.1f In" % pressure_inhg)
    #print("Altitude: %0.2f feet" % (sensor.altitude * 3.2808))

    return errors
errors = []
try:
    sensor_errors = readPressureSensors()
    errors.extend(sensor_errors)
except Exception as e:
    errors.append(getExceptionInfo(e))

if len(errors):
    if 'gmail' in config:
        sendAlertEmail(errors)
    print('\n'.join(errors))
