#!/usr/bin/env python

import os
import sys
import glob
import traceback
import re
import smtplib
import sqlite3
import time
from config import config
from commands import getstatusoutput

DIR = os.path.dirname(os.path.realpath(__file__))
db_filename = 'sensor_values.db'
db_filepath = os.path.join(DIR, 'database', db_filename)

db_is_new = not os.path.exists(db_filepath)
conn = sqlite3.connect(db_filepath)

modules = open('/proc/modules').read()
if 'w1_therm' not in modules:
    getstatusoutput('sudo modprobe w1-therm')
if 'w1_gpio' not in modules:
    getstatusoutput('sudo modprobe w1-gpio')

def provisionDatabase():
    schema_filepath = os.path.join(DIR, 'sensor_values_schema.sql')
    with open(schema_filepath, 'rt') as f:
        schema = f.read()
        conn.executescript(schema)
    populateInitialSensorData()

def populateInitialSensorData():
    cur = conn.cursor()
    for serial_code in config['temp_sensors']:
        sensor = config['temp_sensors'][serial_code]
        name = sensor['name']
        cur.execute('INSERT INTO sensors \
                        (serial_code, name) \
                     VALUES \
                        (?, ?)',
                        (serial_code, name))
        conn.commit()

def getExceptionInfo(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    path = exc_tb.tb_frame.f_code.co_filename
    fname = os.path.split(path)[1]
    fdir = os.path.split(os.path.dirname(path))[1]
    return str(e)+'\n'+''.join(traceback.format_tb(exc_tb))

def sendAlertEmail(errors):
    username = config['gmail']['username']
    password = config['gmail']['password']
    msg = "Subject: [ALERT] %s\n\n%s\n\n%s" % (errors[0], "\n".join(errors), config['gmail']['site_url'])
    fromaddr = config['gmail']['from_address']
    toaddrs = config['gmail']['to_addresses']

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def getSensorSerialCodeMap():
    sensors = {}
    cur = conn.cursor()
    cur.execute('SELECT \
                     id, serial_code, name \
                 FROM sensors WHERE deleted = 0;')
    for row in cur.fetchall():
        sensors[row[1]] = {
                'id': row[0],
                'serial_code': row[1],
                'name': row[2]
            }
    return sensors

def getSensorBySerialCode(serial_code):
    cur = conn.cursor()
    cur.execute('SELECT \
                     id, serial_code, name \
                 FROM sensors WHERE deleted = 0 and serial_code = ?;',
                 (serial_code,))
    row = cur.fetchone()
    return {
        'id': row[0],
        'serial_code': row[1],
        'name': row[2]
    }

def addTemp(serial_code, value):
    sensor = getSensorBySerialCode(serial_code)
    cur = conn.cursor()
    cur.execute('INSERT INTO sensor_readings (sensor_id, value) VALUES (?, ?)',
                    (sensor['id'], value))
    conn.commit()

def readSensors():
    errors = []
    temps = ['NaN']*len(config['temp_sensors'])
    for file_path in glob.glob('/sys/bus/w1/devices/28-*'):
        sensor_id = os.path.basename(file_path)
        if sensor_id not in config['temp_sensors']:
            errors.append("%s not found in config" % sensor_id)
            continue
        sensor_config = config['temp_sensors'][sensor_id]
        data_file_path = file_path+'/w1_slave'
        failed_read_attempts = 0
        while failed_read_attempts < 5:
            f = open(data_file_path, 'r')
            line_1 = f.readline().rstrip()
            line_2 = f.readline().rstrip()
            status_re = re.search("(\w*)$", line_1)
            if status_re:
                status_match = status_re.group(0)
                status = (status_match == 'YES')
                if status:
                    temp_re = re.search("t=(-?\d*)$", line_2)
                    if temp_re:
                        temp_str = temp_re.group(1)
                        temp_c = float(temp_str)/1000
                        temp_f = (temp_c * 9/5) + 32
                        addTemp(sensor_id, temp_f)
                        rrd_order = config['temp_sensors'][sensor_id]['rrd_order']
                        temps[rrd_order-1] = temp_f
                        if 'alert_threshold' in sensor_config and sensor_config['alert_threshold']:
                            threshold = sensor_config['alert_threshold']
                            if temp_f < threshold:
                                errors.append("%s current temp %s is below threshold of %s" % (sensor_config['name'], temp_f, threshold))
                        break
                    else:
                        errors.append('Error matching temp in %s' % data_file_path)
                else:
                    errors.append('Error reading temp from %s sensor %s (%s)' % (sensor_config['name'], sensor_id, status_match))
            else:
                errors.append('Error matching status in %s' % data_file_path)
            failed_read_attempts += 1
            time.sleep(2)
        if failed_read_attempts >= 5:
            errors.append('5 failed read attempts for %s' % sensor_config['name'])

    if 'NaN' in temps:
        errors.append('One or more temperature sensors missing')
        working_sensors = [os.path.basename(x) for x in glob.glob('/sys/bus/w1/devices/28-*')]
        missing_sensors = [x for x in config['temp_sensors'].keys() if x not in working_sensors]
        for x in missing_sensors:
            errors.append('%s sensor missing' % config['temp_sensors'][x]['name'])
    
    rrd_path = os.path.join(DIR, 'database', 'temp.rrd')
    temp_values = ':'.join(map(str, temps))
    command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, temp_values)
    status, message = getstatusoutput(command)
    if status != 0:
        errors.append('Error running %s - %d - %s' % (command, status, message))
    
    return errors

def getDailySensorReadingMetrics():
    cur = conn.cursor()
    cur.execute("SELECT * FROM daily_sensor_metrics ORDER BY current desc;")
    colwidth = 15
    print 'Name'.ljust(colwidth) \
            +'Current'.ljust(colwidth) \
            +'Average'.ljust(colwidth) \
            +'Min'.ljust(colwidth) \
            +'Max'.ljust(colwidth)
    for row in cur.fetchall():
        print row[0].ljust(colwidth) \
                + str(row[1]).ljust(colwidth) \
                + str(row[2]).ljust(colwidth) \
                + str(row[3]).ljust(colwidth) \
                + str(row[4]).ljust(colwidth) \

if db_is_new:
    provisionDatabase()

errors = []
try:
    sensor_errors = readSensors()
    errors.extend(sensor_errors)
except Exception, e:
    errors.append(getExceptionInfo(e))

if len(errors):
    if 'gmail' in config:
        sendAlertEmail(errors)
    print '\n'.join(errors)

#getDailySensorReadingMetrics()
