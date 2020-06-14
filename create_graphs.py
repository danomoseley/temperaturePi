#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from config import config
import collections
from subprocess import getstatusoutput
import time

DIR = os.path.dirname(os.path.realpath(__file__))

temp_sensors = config['temp_sensors']
sorted_temp_sensor_ids = sorted(temp_sensors, key=lambda key: temp_sensors[key]['display_order'])
sorted_temp_sensors = [temp_sensors[k] for k in sorted_temp_sensor_ids]

humidity_sensors = config['humidity_sensors']
sorted_humidity_sensor_ids = sorted(humidity_sensors, key=lambda key: humidity_sensors[key]['display_order'])
sorted_humidity_sensors = [humidity_sensors[k] for k in sorted_humidity_sensor_ids]

lake_temp_sensors = config['lake_temp_sensors']
sorted_lake_temp_sensor_ids = sorted(lake_temp_sensors, key=lambda key: lake_temp_sensors[key]['display_order'])
sorted_lake_temp_sensors = [lake_temp_sensors[k] for k in sorted_lake_temp_sensor_ids]

graphs = [
    {
        'rrd_path': os.path.join(DIR, 'database', 'temp.rrd'),
        'vertical_label': 'Temperature (°F)',
        'unit': '°',
        'sensors': sorted_temp_sensors,
        'variations': [
            {
                'filename': 'temp_hourly.png',
                'title': 'Temperature Last 4 Hours',
                'start': '-14400'
            },
            {
                'filename': 'temp_hourly_mobile.png',
                'title': 'Temperature Last 4 Hours',
                'start': '-14400',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'temp_daily.png',
                'title': 'Temperature Last 24 Hours',
                'start': '-1d'
            },
            {
                'filename': 'temp_daily_mobile.png',
                'title': 'Temperature Last 24 Hours',
                'start': '-1d',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'temp_weekly.png',
                'title': 'Weekly Temperature',
                'start': '-1w'
            },
            {
                'filename': 'temp_weekly_mobile.png',
                'title': 'Weekly Temperature',
                'start': '-1w',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'temp_monthly.png',
                'title': 'Monthly Temperature',
                'start': '-1m'
            },
            {
                'filename': 'temp_monthly_mobile.png',
                'title': 'Monthly Temperature',
                'start': '-1m',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'temp_yearly.png',
                'title': 'Yearly Temperature',
                'start': '-1y'
            },
            {
                'filename': 'temp_yearly_mobile.png',
                'title': 'Yearly Temperature',
                'start': '-1y',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
       ]
    },
    {
        'rrd_path': os.path.join(DIR, 'database', 'humidity.rrd'),
        'vertical_label': 'Relative Humidity (%)',
        'unit': '%%',
        'sensors': sorted_humidity_sensors,
        'variations': [
            {
                'filename': 'humidity_hourly.png',
                'title': 'Humidity Last 4 Hours',
                'start': '-14400'
            },
            {
                'filename': 'humidity_hourly_mobile.png',
                'title': 'Humidity Last 4 Hours',
                'start': '-14400',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'humidity_daily.png',
                'title': 'Humidity Last 24 Hours',
                'start': '-1d'
            },
            {
                'filename': 'humidity_daily_mobile.png',
                'title': 'Humidity Last 24 Hours',
                'start': '-1d',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'humidity_weekly.png',
                'title': 'Weekly Humidity',
                'start': '-1w'
            },
            {
                'filename': 'humidity_weekly_mobile.png',
                'title': 'Weekly Humidity',
                'start': '-1w',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'humidity_monthly.png',
                'title': 'Monthly Humidity',
                'start': '-1m'
            },
            {
                'filename': 'humidity_monthly_mobile.png',
                'title': 'Monthly Humidity',
                'start': '-1m',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
            {
                'filename': 'humidity_yearly.png',
                'title': 'Yearly Humidity',
                'start': '-1y'
            },
            {
                'filename': 'humidity_yearly_mobile.png',
                'title': 'Yearly Humidity',
                'start': '-1y',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            },
        ]
    },
    {
        'rrd_path': os.path.join(DIR, 'database', 'lake_temp.rrd'),
        'vertical_label': 'Temperature (°F)',
        'unit': '°',
        'sensors': sorted_lake_temp_sensors,
        'variations': [
            {
                'filename': 'lake_temp_hourly.png',
                'title': 'Lake Temperature Last 4 Hours',
                'start': '-14400'
            },
            {
                'filename': 'lake_temp_daily.png',
                'title': 'Lake Temperature Last 24 Hours',
                'start': '-1d'
            },
            {
                'filename': 'lake_temp_weekly.png',
                'title': 'Weekly Lake Temperature',
                'start': '-1w'
            },
            {
                'filename': 'lake_temp_monthly.png',
                'title': 'Monthly Lake Temperature',
                'start': '-1m'
            },
            {
                'filename': 'lake_temp_yearly.png',
                'title': 'Yearly Lake Temperature',
                'start': '-1y'
            },
            {
                'filename': 'lake_temp_daily_mobile.png',
                'title': 'Lake Temperature Last 24 Hours',
                'start': '-1d',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 29,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            }
        ]
    },
]

directory = os.path.join(DIR, 'latest_graphs')

if not os.path.exists(directory):
    os.makedirs(directory)

overall_tic = time.perf_counter()
for graph in graphs:
    if os.path.isfile(graph['rrd_path']) and len(graph['sensors']):
        max_name_length = 0
        for sensor in graph['sensors']:
            name_length = len(sensor['name'])
            if name_length > max_name_length:
                max_name_length = name_length
        max_name_length += 2
        for graph_variation in graph['variations']:
            if 'title_font' not in graph_variation:
                graph_variation['title_font'] = 12
            if 'axis_font' not in graph_variation:
                graph_variation['axis_font'] = 8
            if 'legend_font' not in graph_variation:
                graph_variation['legend_font'] = 10
            if 'unit_font' not in graph_variation:
                graph_variation['unit_font'] = 8
            if 'padding' not in graph_variation:
                graph_variation['padding'] = 10
            if 'line_stroke' not in graph_variation:
                graph_variation['line_stroke'] = 2

            padding = graph_variation['padding']
            label = 'NOW'.rjust(padding+3)+'MIN'.rjust(padding+4)+'MAX'.rjust(padding+3)+'AVG'.rjust(padding+4)
            command = '''
            rrdtool graph %s/%s \\
            -w 1024 -h 500 -a PNG \\
            --title='%s' \\
            --font TITLE:%d: \\
            --font AXIS:%d: \\
            --font LEGEND:%d: \\
            --font UNIT:%d: \\
            --slope-mode \\
            --start %s --end now \\
            --vertical-label '%s' \\
            COMMENT:'%s\\n' \\
            ''' % (directory, graph_variation['filename'], graph_variation['title'], \
                graph_variation['title_font'], graph_variation['axis_font'], \
                graph_variation['legend_font'], graph_variation['unit_font'], \
                graph_variation['start'], graph['vertical_label'], \
                label.rjust(len(label) + max_name_length))

            for sensor in graph['sensors']:
                display_name = sensor['name'] + '\:'
                command += '''DEF:%(ds_name)s=%(rrd_path)s:%(ds_name)s:AVERAGE \\
                    LINE%(line_stroke)d:%(ds_name)s%(color)s:'%(display_name)s' \\
                    GPRINT:%(ds_name)s:LAST:'%%%(padding)d.1lf%(unit)s' \\
                    GPRINT:%(ds_name)s:MIN:'%%%(padding)d.1lf%(unit)s' \\
                    GPRINT:%(ds_name)s:MAX:'%%%(padding)d.1lf%(unit)s' \\
                    GPRINT:%(ds_name)s:AVERAGE:'%%%(padding)d.1lf%(unit)s\\n' \\
                    ''' % {
                            'ds_name': sensor['ds_name'],
                            'rrd_path': graph['rrd_path'],
                            'line_stroke': graph_variation['line_stroke'],
                            'color': sensor['color'],
                            'display_name': display_name.ljust(max_name_length),
                            'padding': padding,
                            'unit': graph['unit']
                          }
            command += '''"COMMENT:\\n" \\
                "COMMENT:$(date "+%m/%d/%y %l:%M %p" | sed 's/:/\\\:/g')"'''

            if graph_variation['title'] == "Temperature Last 24 Hours":
                if config.get("thermostat_away", False):
                    command += "' | AWAY'"
                if config.get("thermostat_out", False):
                    command += "' | OUT'"

            #print(command)
            tic = time.perf_counter()
            status = getstatusoutput(command)
            toc = time.perf_counter()
            print(f"{graph_variation['filename']} took {toc - tic:0.4f} seconds")

            print(status)

overall_toc = time.perf_counter()
print(f"Graph generation took {overall_toc - overall_tic:0.4f} seconds")
