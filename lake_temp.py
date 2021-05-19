#!/usr/bin/env python3

from bs4 import BeautifulSoup
import temperature
import requests
import os
import math
import pprint
from subprocess import getstatusoutput
from utils import sendAlertEmail
from utils import dbConnection
from utils import convert_c_to_f, getExceptionInfo
from config import config

DIR = os.path.dirname(os.path.realpath(__file__))

class BuoyOfflineError(Exception):
    pass

def setBuoyOffline(offline=True):
    pp = pprint.PrettyPrinter(indent=4)
    config['lake_temp_buoy_offline'] = offline
    f = open(os.path.join(DIR, 'config.py'), 'w')
    f.write('config = %s' % pp.pformat(config))

def getReadings():
    r  = requests.get("https://www.wqdatalive.com/project/applet/html/831")
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    readings = {}

    for row in table.find_all("tr"):
        if not row.has_attr("class"):
            tds = row.find_all('td')
            param = tds[0].contents[0].lower().replace(" ","_").replace(".","")
            value = float(tds[1].contents[0].lower().replace(" ","_"))
            units = tds[2].contents[0].lower().replace(" ","_")
            if units == "c":
                if value == -100000.00:
                    setBuoyOffline(True)
                    raise BuoyOfflineError("Lake temp -100000.00c (error state), buoy set to offline")
                value = convert_c_to_f(value)
                units = "f"
            value = math.floor(value*10)/10
            readings[param] = (value, units)

    return readings

def populateInitialSensorData():
    conn = dbConnection()
    cur = conn.cursor()
    readings = getReadings()
    for serial_code in readings:
        cur.execute('INSERT INTO sensors \
                        (serial_code, name) \
                     VALUES \
                        (?, ?)',
                        (serial_code, serial_code))
        conn.commit()

def writeReadingsToDb(readings):
    for serial_code in readings:
        temperature.addTemp(serial_code, readings[serial_code][0])

def writeReadingsToRrd(readings):
    errors = []
    try:
        temps = ['NaN']*len(config['lake_temp_sensors'])

        for sensor_id in config['lake_temp_sensors']:
            rrd_order = config['lake_temp_sensors'][sensor_id]['rrd_order']
            if sensor_id in readings:
                temps[rrd_order-1] = readings[sensor_id][0]

        rrd_path = os.path.join(DIR, 'database', 'lake_temp.rrd')
        temp_values = ':'.join(map(str, temps))
        command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, temp_values)
        status, message = getstatusoutput(command)
        if status != 0:
            errors.append('Error running %s - %d - %s' % (command, status, message))
    except Exception as e:
        errors.append(getExceptionInfo(e))

    if len(errors):
        if 'gmail' in config:
            sendAlertEmail(errors)
        print('\n'.join(errors))

def writeWindReadingsToRrd(readings):
    errors = []
    try:
        temps = ['NaN']*len(config['wind_speed_sensors'])

        for sensor_id in config['wind_speed_sensors']:
            rrd_order = config['wind_speed_sensors'][sensor_id]['rrd_order']
            if sensor_id in readings:
                temps[rrd_order-1] = readings[sensor_id][0]

        rrd_path = os.path.join(DIR, 'database', 'wind_speed.rrd')
        values = ':'.join(map(str, temps))
        command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, values)
        status, message = getstatusoutput(command)
        if status != 0:
            errors.append('Error running %s - %d - %s' % (command, status, message))
    except Exception as e:
        errors.append(getExceptionInfo(e))

    if len(errors):
        if 'gmail' in config:
            sendAlertEmail(errors)
        print('\n'.join(errors))

#This runs once per hour to check if an offline buoy is back
def checkBuoy():
    if not config.get('lake_temp_sensors_disabled', True):
        if config.get('lake_temp_buoy_offline', False):
            try:
                readings = getReadings()
                if readings:
                    setBuoyOffline(False)
                    sendAlertEmail(["Buoy is back! Set to online"])
            except BuoyOfflineError:
                pass

def process():
    lake_temp_sensors_disabled = config.get('lake_temp_sensors_disabled', True)
    lake_temp_buoy_offline = config.get('lake_temp_buoy_offline', False)
    if not lake_temp_sensors_disabled and not lake_temp_buoy_offline:
        readings = getReadings()
        writeReadingsToRrd(readings)
        writeReadingsToDb(readings)
        writeWindReadingsToRrd(readings)
        checkCalmness()

def setCalmAlarmState(in_alarm=True):
    pp = pprint.PrettyPrinter(indent=4)
    config['lake_calm_in_alarm'] = in_alarm
    f = open(os.path.join(DIR, 'config.py'), 'w')
    f.write('config = %s' % pp.pformat(config))

def checkCalmness():
    conn = dbConnection()
    cur = conn.cursor()
    cur.execute("SELECT avg(value) FROM sensor_readings WHERE sensor_id=58 and datetime(timestamp) > datetime('now', '-1 hour')")
    wind_speed = cur.fetchone()[0]
    calm_in_alarm = config.get('lake_calm_in_alarm', False)
    # This is in meters per second
    wind_threshold = 1
    print(wind_speed)
    if wind_speed < wind_threshold:
        if not calm_in_alarm:
            sendAlertEmail(["The lake is very calm!", f"{wind_speed:.1f} m/s average over the past hour"])
            setCalmAlarmState(True)
    elif calm_in_alarm:
        setCalmAlarmState(False)

if __name__ == "__main__":
    process()

