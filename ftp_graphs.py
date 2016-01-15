#!/usr/bin/python
import paramiko
import os
from commands import getstatusoutput
 
DIR = os.path.dirname(os.path.realpath(__file__))
 
#generate graphs
getstatusoutput(DIR + '/get_temp.pl')
getstatusoutput(DIR + '/get_humidity.pl')

getstatusoutput(DIR + '/create_graphs_temp.sh')
getstatusoutput(DIR + '/create_graphs_humidity.sh') 
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('direct.danomoseley.com', username='dan')
 
sftp = ssh.open_sftp();
sftp.put(DIR + '/latest_graphs/temp_hourly.png', '/var/www/camp/temp_hourly.png')
sftp.put(DIR + '/latest_graphs/temp_daily.png', '/var/www/camp/temp_daily.png')
sftp.put(DIR + '/latest_graphs/temp_daily_mobile.png', '/var/www/camp/temp_daily_mobile.png')
sftp.put(DIR + '/latest_graphs/temp_weekly.png', '/var/www/camp/temp_weekly.png')
sftp.put(DIR + '/latest_graphs/temp_monthly.png', '/var/www/camp/temp_monthly.png')
sftp.put(DIR + '/latest_graphs/temp_yearly.png', '/var/www/camp/temp_yearly.png')

sftp.put(DIR + '/latest_graphs/humidity_hourly.png', '/var/www/camp/humidity_hourly.png')
sftp.put(DIR + '/latest_graphs/humidity_daily.png', '/var/www/camp/humidity_daily.png')
sftp.put(DIR + '/latest_graphs/humidity_daily_mobile.png', '/var/www/camp/humidity_daily_mobile.png')
sftp.put(DIR + '/latest_graphs/humidity_weekly.png', '/var/www/camp/humidity_weekly.png')
sftp.put(DIR + '/latest_graphs/humidity_monthly.png', '/var/www/camp/humidity_monthly.png')
sftp.put(DIR + '/latest_graphs/humidity_yearly.png', '/var/www/camp/humidity_yearly.png')

sftp.close()

