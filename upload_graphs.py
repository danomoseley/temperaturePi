#!/usr/bin/python3
import os
from subprocess import getstatusoutput
from config import config
from datetime import datetime, timedelta
import time
import temperature
import lake_temp
import pressure
import humidity
import graphs

import boto3

DIR = os.path.dirname(os.path.realpath(__file__))

def roundDownDatetime(dt):
    delta_min = dt.minute % 5
    return datetime(dt.year, dt.month, dt.day,
                             dt.hour, dt.minute - delta_min)

overall_tic = time.perf_counter()

if os.path.isfile(os.path.join(DIR, 'database', 'temp.rrd')):
    tic = time.perf_counter()
    temperature.process()
    toc = time.perf_counter()
    print(f"Temperature processing took {toc - tic:0.4f} seconds")

if os.path.isfile(os.path.join(DIR, 'database', 'humidity.rrd')):
    tic = time.perf_counter()
    humidity.process()
    toc = time.perf_counter()
    print(f"Humidity processing took {toc - tic:0.4f} seconds")


if os.path.isfile(os.path.join(DIR, 'database', 'pressure.rrd')):
    tic = time.perf_counter()
    pressure.process()
    toc = time.perf_counter()
    print(f"Pressure processing took {toc - tic:0.4f} seconds")


if os.path.isfile(os.path.join(DIR, 'database', 'lake_temp.rrd')):
    tic = time.perf_counter()
    lake_temp.process()
    toc = time.perf_counter()
    print(f"Lake Temp processing took {toc - tic:0.4f} seconds")

graphs.createGraphs(daily=True)

expires = datetime.utcnow() + timedelta(minutes=5)
expires = roundDownDatetime(expires)

directory = os.path.join(DIR, 'latest_graphs')

s3 = boto3.resource('s3')
s3_bucket = config['s3_bucket']

tic = time.perf_counter()
files = os.listdir(directory)
for file in files:
    file_path = os.path.join(directory, file)
    s3.Bucket(s3_bucket).upload_file(file_path, f"latest_graphs/{file}", ExtraArgs={'Expires':expires})

toc = time.perf_counter()

print(f"Daily graphs upload took {toc - tic:0.4f} seconds")

expires_15_minutes = datetime.utcnow() + timedelta(minutes=15)
expires_15_minutes = roundDownDatetime(expires_15_minutes)

now = datetime.now()
create_weekly = (now.minute < 5 or 15 <= now.minute < 20 or 30 <= now.minute < 35 or 45 <= now.minute < 50)
create_monthly = (5 <= now.minute < 10 or 20 <= now.minute < 25 or 35 <= now.minute < 40 or 50 <= now.minute < 55)
create_yearly = (10 <= now.minute < 15 or 25 <= now.minute < 30 or 40 <= now.minute < 45 or 55 <= now.minute)

if create_weekly or create_monthly or create_yearly:
    graphs.createGraphs(daily=False, weekly=create_weekly, monthly=create_monthly, yearly=create_yearly)

    tic = time.perf_counter()
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        s3.Bucket(s3_bucket).upload_file(file_path, f"latest_graphs/{file}",ExtraArgs={'Expires':expires_15_minutes})

    toc = time.perf_counter()

    print(f"Extra graph uploads took {toc - tic:0.4f} seconds")

if os.path.isfile(os.path.join(DIR, 'database', 'lake_temp.rrd')):
    tic = time.perf_counter()
    lake_temp.checkCalmness()
    toc = time.perf_counter()
    print(f"Check lake calmness took {toc - tic:0.4f} seconds")

overall_toc = time.perf_counter()
print(f"Total processing took {overall_toc - overall_tic:0.4f} seconds")

