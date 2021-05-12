#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import os
import math
import pprint
from subprocess import getstatusoutput
from utils import sendAlertEmail
from utils import convert_c_to_f
from config import config

DIR = os.path.dirname(os.path.realpath(__file__))

class BuoyOfflineError(Exception):
    pass

def set_buoy_offline(offline=True):
    pp = pprint.PrettyPrinter(indent=4)
    config['lake_temp_buoy_offline'] = offline
    f = open(os.path.join(DIR, 'config.py'), 'w')
    f.write('config = %s' % pp.pformat(config))

def get_readings():
    r  = requests.get("https://v2.wqdatalive.com/project/applet/html/831")
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
                    set_buoy_offline(True)
                    raise BuoyOfflineError("Lake temp -100000.00c (error state), buoy set to offline")
                value = convert_c_to_f(value)
                units = "f"
            value = math.floor(value*10)/10
            if value > -100 and value < 120:
                readings[param] = (value, units)

    return readings

def write_readings_to_rrd():
    errors = []
    try:
        readings = get_readings()
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
    except Exception, e:
        errors.append(getExceptionInfo(e))

    if len(errors):
        if 'gmail' in config:
            sendAlertEmail(errors)
        print('\n'.join(errors))

#This runs once per hour to check if an offline buoy is back
def check_buoy():
    if not config.get('lake_temp_sensors_disabled', True):
        if config.get('lake_temp_buoy_offline', False):
            try:
                readings = get_readings()
                if readings:
                    set_buoy_offline(False)
                    sendAlertEmail(["Buoy is back! Set to online"])
            except BuoyOfflineError:
                pass

lake_temp_sensors_disabled = config.get('lake_temp_sensors_disabled', False)
if not lake_temp_sensors_disabled:
    write_readings_to_rrd()

