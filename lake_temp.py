#!/usr/bin/env python3

from bs4 import BeautifulSoup
from subprocess import getstatusoutput

import temperature
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError
import os
import math
import pprint
import time
import utils
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
    try:
        r  = requests.get("https://www.wqdatalive.com/project/applet/html/831", timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")
        readings = {}

        for row in table.find_all("tr"):
            if not row.has_attr("class"):
                tds = row.find_all('td')
                param = tds[0].contents[0].lower().replace(" ","_").replace(".","")
                value = float(tds[1].contents[0].lower().replace(" ","_"))
                units = tds[2].contents[0].lower().replace(" ","_")
                if param in readings:
                    param += "_"+units
                if units == "c":
                    if value == -100000.00:
                        setBuoyOffline(True)
                        raise BuoyOfflineError("Lake temp -100000.00c (error state), buoy set to offline")
                    value = utils.convert_c_to_f(value)
                    units = "f"
                value = math.floor(value*10)/10
                readings[param] = (value, units)

        return readings
    except (ConnectionError, ConnectTimeout, ReadTimeout) as error:
        setBuoyOffline(True)
        raise BuoyOfflineError("Lake temp connection timeout, buoy set to offline")

def populateInitialSensorData():
    conn = utils.dbConnection()
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

#This runs once per hour to check if an offline buoy is back
def checkBuoy():
    if not config.get('lake_temp_sensors_disabled', True):
        if config.get('lake_temp_buoy_offline', False):
            try:
                readings = getReadings()
                if readings:
                    setBuoyOffline(False)
                    utils.sendAlertEmail(["Buoy is back! Set to online"])
            except BuoyOfflineError:
                pass

def process():
    lake_temp_sensors_disabled = config.get('lake_temp_sensors_disabled', True)
    lake_temp_buoy_offline = config.get('lake_temp_buoy_offline', False)
    if not lake_temp_sensors_disabled and not lake_temp_buoy_offline:
        errors = []
        try:
            tic = time.perf_counter()
            readings = getReadings()
            toc = time.perf_counter()
            print(f"getReadings took {toc - tic:0.4f} seconds")

            errors.extend(utils.writeReadingsToRrd('lake_temp.rrd', config['lake_temp_sensors'], readings))
            tic = time.perf_counter()
            writeReadingsToDb(readings)
            toc = time.perf_counter()
            print(f"writeReadingsToDb took {toc - tic:0.4f} seconds")

            errors.extend(utils.writeReadingsToRrd('wind_speed.rrd', config['wind_speed_sensors'], readings))
            
        except BuoyOfflineError as e:
            errors.append(str(e))
        if len(errors):
            if 'gmail' in config:
                utils.sendAlertEmail(errors)
            print('\n'.join(errors))

def setCalmAlarmState(in_alarm=True):
    pp = pprint.PrettyPrinter(indent=4)
    config['lake_calm_in_alarm'] = in_alarm
    f = open(os.path.join(DIR, 'config.py'), 'w')
    f.write('config = %s' % pp.pformat(config))

def checkCalmness():
    conn = utils.dbConnection()
    cur = conn.cursor()
    cur.execute("SELECT avg(value) FROM sensor_readings WHERE sensor_id=58 and datetime(timestamp) > datetime('now', '-1 hour')")
    wind_speed = cur.fetchone()[0]
    calm_in_alarm = config.get('lake_calm_in_alarm', False)
    # This is in meters per second
    wind_threshold = 1
    print(wind_speed)
    if wind_speed < wind_threshold:
        if not calm_in_alarm:
            utils.sendAlertEmail(["The lake is very calm!", f"{wind_speed:.1f} m/s average over the past hour"])
            setCalmAlarmState(True)
    elif calm_in_alarm:
        setCalmAlarmState(False)

if __name__ == "__main__":
    process()

