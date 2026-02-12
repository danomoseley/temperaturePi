#!/usr/bin/python3
import json
import os
from subprocess import getstatusoutput
from config import config
from datetime import datetime, timedelta
import time
import temperature
import lake_temp
import pressure
import humidity
import radon
import graphs

import boto3

def roundDownDatetime(dt):
    delta_min = dt.minute % 5
    return datetime(dt.year, dt.month, dt.day,
                             dt.hour, dt.minute - delta_min)

def process(create_weekly=None, create_monthly=None, create_yearly=None, process_radon_sensors=None, create_radon_extras=None):
    DIR = os.path.dirname(os.path.realpath(__file__))
    overall_tic = time.perf_counter()

    start_time = datetime.now()
    
    data = {}

    if process_radon_sensors is None:
        process_radon_sensors = start_time.minute < 5

    if os.path.isfile(os.path.join(DIR, 'database', 'temp.rrd')):
        tic = time.perf_counter()
        data["temperature"] = temperature.process()
        toc = time.perf_counter()
        print(f"Temperature processing took {toc - tic:0.4f} seconds")

    if os.path.isfile(os.path.join(DIR, 'database', 'humidity.rrd')):
        tic = time.perf_counter()
        data["humidity"] = humidity.process()
        toc = time.perf_counter()
        print(f"Humidity processing took {toc - tic:0.4f} seconds")

    if os.path.isfile(os.path.join(DIR, 'database', 'pressure.rrd')):
        tic = time.perf_counter()
        data["pressure"] = pressure.process()
        toc = time.perf_counter()
        print(f"Pressure processing took {toc - tic:0.4f} seconds")

    if 'mqtt' in config and 'host' in config['mqtt']:
        site_slug = config['site_display_name'].lower().replace(' ', '_')
        command = '/usr/bin/mosquitto_pub -t temperaturePi/%s/sensors -h %s -m \'%s\'' % (site_slug, config['mqtt']['host'], json.dumps(data))
        status, message = getstatusoutput(command)
        if status != 0:
            errors.append('Error running %s - %d - %s' % (command, status, message))

    if os.path.isfile(os.path.join(DIR, 'database', 'radon.rrd')):
        if process_radon_sensors:
            tic = time.perf_counter()
            radon.process()
            toc = time.perf_counter()
            print(f"Radon processing took {toc - tic:0.4f} seconds")
        else:
            print("Skipping radon processing")

    if os.path.isfile(os.path.join(DIR, 'database', 'lake_temp.rrd')):
        tic = time.perf_counter()
        lake_temp.process()
        toc = time.perf_counter()
        print(f"Lake Temp processing took {toc - tic:0.4f} seconds")

    graphs.createGraphs(daily=True, radon=process_radon_sensors)

    expires = datetime.utcnow() + timedelta(minutes=5)
    expires = roundDownDatetime(expires)

    expires_1_hour = datetime.utcnow() + timedelta(hours=1)
    expires_1_hour = roundDownDatetime(expires_1_hour)

    directory = os.path.join(DIR, 'latest_graphs')

    s3 = boto3.resource('s3')
    s3_bucket = config['s3_bucket']

    tic = time.perf_counter()
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        upload_expires = expires
        if 'radon' in file:
            upload_expires = expires_1_hour
        s3.Bucket(s3_bucket).upload_file(file_path, f"latest_graphs/{file}", ExtraArgs={'Expires':upload_expires,'ContentType':'image/png'})

    toc = time.perf_counter()

    print(f"Daily graphs upload took {toc - tic:0.4f} seconds")

    expires_15_minutes = datetime.utcnow() + timedelta(minutes=15)
    expires_15_minutes = roundDownDatetime(expires_15_minutes)

    if create_radon_extras is None:
        create_radon_extras = start_time.minute < 15
    if create_weekly is None:
        create_weekly = (start_time.minute < 5 or 15 <= start_time.minute < 20 or 30 <= start_time.minute < 35 or 45 <= start_time.minute < 50)
    if create_monthly is None:
        create_monthly = (5 <= start_time.minute < 10 or 20 <= start_time.minute < 25 or 35 <= start_time.minute < 40 or 50 <= start_time.minute < 55)
    if create_yearly is None:
        create_yearly = (10 <= start_time.minute < 15 or 25 <= start_time.minute < 30 or 40 <= start_time.minute < 45 or 55 <= start_time.minute)

    if create_weekly or create_monthly or create_yearly:
        graphs.createGraphs(daily=False, weekly=create_weekly, monthly=create_monthly, yearly=create_yearly, radon=create_radon_extras)

        tic = time.perf_counter()
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            upload_expires = expires_15_minutes
            if 'radon' in file:
                upload_expires = expires_1_hour
            s3.Bucket(s3_bucket).upload_file(file_path, f"latest_graphs/{file}",ExtraArgs={'Expires':upload_expires,'ContentType':'image/png'})

        toc = time.perf_counter()

        print(f"Extra graph uploads took {toc - tic:0.4f} seconds")

    if os.path.isfile(os.path.join(DIR, 'database', 'lake_temp.rrd')):
        tic = time.perf_counter()
        lake_temp.checkCalmness()
        toc = time.perf_counter()
        print(f"Check lake calmness took {toc - tic:0.4f} seconds")

    overall_toc = time.perf_counter()
    print(f"Total processing took {overall_toc - overall_tic:0.4f} seconds")

if __name__ == '__main__':
    process()

