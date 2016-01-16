#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from config import config
import collections
from commands import getstatusoutput

DIR = os.path.dirname(os.path.realpath(__file__))

sorted_temp_sensors = sorted(config['temp_sensors'], key=lambda key: config['temp_sensors'][key]['display_order'])

max_name_length = 0
for sensor_id in sorted_temp_sensors:
    name_length = len(config['temp_sensors'][sensor_id]['name'])
    if name_length > max_name_length:
        max_name_length = name_length
max_name_length += 2

graphs = [
    {
        'filename': 'temp_hourly_test.png',
        'title': 'Temperature Last 4 Hours',
        'start': '-14400'
    },
    {
        'filename': 'temp_daily_test.png',
        'title': 'Temperature Last 24 Hours',
        'start': '-1d'
    },
    {
        'filename': 'temp_weekly_test.png',
        'title': 'Weekly Temperature',
        'start': '-1w'
    },
    {
        'filename': 'temp_monthly_test.png',
        'title': 'Monthly Temperature',
        'start': '-1m'
    },
    {
        'filename': 'temp_yearly_test.png',
        'title': 'Yearly Temperature',
        'start': '-1y'
    },
    {
        'filename': 'temp_daily_mobile_test.png',
        'title': 'Temperature Last 24 Hours',
        'start': '-1d',
        'title_font': 30,
        'axis_font': 17,
        'legend_font': 30,
        'unit_font': 20,
        'pad': 4,
        'line_stroke': 8
    }
]

for graph in graphs:
    if 'title_font' not in graph:
        graph['title_font'] = 12
    if 'axis_font' not in graph:
        graph['axis_font'] = 8
    if 'legend_font' not in graph:
        graph['legend_font'] = 10
    if 'unit_font' not in graph:
        graph['unit_font'] = 8
    if 'pad' not in graph:
        graph['pad'] = 10
    if 'line_stroke' not in graph:
        graph['line_stroke'] = 2

    label = 'NOW'.rjust(graph['pad']+3)+'MIN'.rjust(graph['pad']+4)+'MAX'.rjust(graph['pad']+3)+'AVG'.rjust(graph['pad']+4)
    command = '''
    rrdtool graph latest_graphs/%s \\
    -w 1024 -h 500 -a PNG \\
    --title='%s' \\
    --font TITLE:%d: \\
    --font AXIS:%d: \\
    --font LEGEND:%d: \\
    --font UNIT:%d: \\
    --slope-mode \\
    --start %s --end now \\
    --vertical-label 'Temperature (°F)' \\
    COMMENT:'%s\\n' \\
    ''' % (graph['filename'], graph['title'], graph['title_font'], graph['axis_font'], \
        graph['legend_font'], graph['unit_font'], graph['start'], label.rjust(len(label)+max_name_length))

    for sensor_id in sorted_temp_sensors:
        ds_name = config['temp_sensors'][sensor_id]['ds_name']
        display_name = config['temp_sensors'][sensor_id]['name'] + '\:'
        color = config['temp_sensors'][sensor_id]['color']

        command += '''DEF:%s=temp.rrd:%s:AVERAGE \\
            LINE%d:%s%s:'%s' \\
            GPRINT:%s:LAST:'%%%d.1lf°' \\
            GPRINT:%s:MIN:'%%%d.1lf°' \\
            GPRINT:%s:MAX:'%%%d.1lf°' \\
            GPRINT:%s:AVERAGE:'%%%d.1lf°\\n' \\
            ''' % (ds_name, ds_name, graph['line_stroke'], ds_name, color, display_name.ljust(max_name_length), \
                ds_name, graph['pad'], ds_name, graph['pad'], ds_name, graph['pad'], ds_name, graph['pad'])
    command += '''"COMMENT:\\n" \\
        "COMMENT:$(date "+%m/%d %l:%M %p" | sed 's/:/\\\:/g')"'''

    #print command
    status = getstatusoutput(command)

    print status
