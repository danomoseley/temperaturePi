#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import os
import math
import pprint
from commands import getstatusoutput
from utils import sendAlertEmail
from utils import convert_c_to_f
from config import config

DIR = os.path.dirname(os.path.realpath(__file__))

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
        print '\n'.join(errors)

lake_temp_sensors_disabled = config.get('lake_temp_sensors_disabled', False)
if not lake_temp_sensors_disabled:
    write_readings_to_rrd()

