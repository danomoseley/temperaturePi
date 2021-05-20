#!/usr/bin/env python3

from config import config
import smtplib
import sqlite3
from datetime import datetime
import sys, os, traceback
from subprocess import getstatusoutput

def sendAlertEmail(errors):
    username = config['gmail']['username']
    password = config['gmail']['password']

    d = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    msg = "Subject: [ALERT] %s\n\n%s\n\n%s\n\n%s" % (errors[0], "\n".join(errors), config['gmail']['site_url'], d)
    fromaddr = config['gmail']['from_address']
    toaddrs = config['gmail']['to_addresses']

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def convert_c_to_f(temp_c):
    return 9.0/5.0 * float(temp_c) + 32.0

def getExceptionInfo(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    path = exc_tb.tb_frame.f_code.co_filename
    fname = os.path.split(path)[1]
    fdir = os.path.split(os.path.dirname(path))[1]
    return str(e)+'\n'+''.join(traceback.format_tb(exc_tb))

class dbConnection(object):
    conn = None

    def __new__(cls):
        if cls.conn is None:
            cls._instance = super(dbConnection, cls).__new__(cls)
            DIR = os.path.dirname(os.path.realpath(__file__))
            db_filename = 'sensor_values.db'
            db_filepath = os.path.join(DIR, 'database', db_filename)
            cls.conn = sqlite3.connect(db_filepath)

        return cls.conn

def writeReadingsToRrd(rrd_filename, sensors_config, readings):
    errors = []
    try:
        values = ['NaN']*len(sensors_config)

        for sensor_id in sensors_config:
            rrd_order = sensors_config[sensor_id]['rrd_order']
            if sensor_id in readings:
                values[rrd_order-1] = readings[sensor_id][0]

        DIR = os.path.dirname(os.path.realpath(__file__))
        rrd_path = os.path.join(DIR, 'database', rrd_filename)
        rrd_data = ':'.join(map(str, values))
        command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, rrd_data)
        status, message = getstatusoutput(command)
        if status != 0:
            errors.append('Error running %s - %d - %s' % (command, status, message))
    except Exception as e:
        errors.append(getExceptionInfo(e))

    return errors

