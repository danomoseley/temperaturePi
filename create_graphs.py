#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from config import config
import collections
from commands import getstatusoutput

DIR = os.path.dirname(os.path.realpath(__file__))

sorted_temp_sensors = [config['temp_sensors'][k] for k in sorted(config['temp_sensors'], key=lambda key: config['temp_sensors'][key]['display_order'])]
sorted_humidity_sensors = [config['humidity_sensors'][k] for k in sorted(config['humidity_sensors'], key=lambda key: config['humidity_sensors'][key]['display_order'])]

graphs = [
    {
        'rrd_path': os.path.join(DIR, 'temp.rrd'),
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
                'filename': 'temp_daily.png',
                'title': 'Temperature Last 24 Hours',
                'start': '-1d'
            },
            {
                'filename': 'temp_weekly.png',
                'title': 'Weekly Temperature',
                'start': '-1w'
            },
            {
                'filename': 'temp_monthly.png',
                'title': 'Monthly Temperature',
                'start': '-1m'
            },
            {
                'filename': 'temp_yearly.png',
                'title': 'Yearly Temperature',
                'start': '-1y'
            },
            {
                'filename': 'temp_daily_mobile.png',
                'title': 'Temperature Last 24 Hours',
                'start': '-1d',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 30,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            }
        ]
    },
    {
        'rrd_path': os.path.join(DIR, 'humidity.rrd'),
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
                'filename': 'humidity_daily.png',
                'title': 'Humidity Last 24 Hours',
                'start': '-1d'
            },
            {
                'filename': 'humidity_weekly.png',
                'title': 'Weekly Humidity',
                'start': '-1w'
            },
            {
                'filename': 'humidity_monthly.png',
                'title': 'Monthly Humidity',
                'start': '-1m'
            },
            {
                'filename': 'humidity_yearly.png',
                'title': 'Yearly Humidity',
                'start': '-1y'
            },
            {
                'filename': 'humidity_daily_mobile.png',
                'title': 'Humidity Last 24 Hours',
                'start': '-1d',
                'title_font': 30,
                'axis_font': 17,
                'legend_font': 30,
                'unit_font': 20,
                'padding': 4,
                'line_stroke': 8
            }
        ]
    }
]

for graph in graphs:
    if os.path.isfile(graph['rrd_path']):
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
            rrdtool graph %s/latest_graphs/%s \\
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
            ''' % (DIR, graph_variation['filename'], graph_variation['title'], \
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
                "COMMENT:$(date "+%m/%d %l:%M %p" | sed 's/:/\\\:/g')"'''

            #print command
            status = getstatusoutput(command)

            print status
