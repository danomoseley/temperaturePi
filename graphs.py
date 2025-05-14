#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from config import config
import collections
from subprocess import getstatusoutput
import time
import temperature

def createGraphs(daily=True, weekly=False, monthly=False, yearly=False):
    DIR = os.path.dirname(os.path.realpath(__file__))

    temp_sensors = config['temp_sensors']
    sorted_temp_sensor_ids = sorted(temp_sensors, key=lambda key: temp_sensors[key]['display_order'])
    sorted_temp_sensors = [temp_sensors[k] for k in sorted_temp_sensor_ids if not temp_sensors[k].get('disabled', False)]

    humidity_sensors = config['humidity_sensors']
    sorted_humidity_sensor_ids = sorted(humidity_sensors, key=lambda key: humidity_sensors[key]['display_order'])
    sorted_humidity_sensors = [humidity_sensors[k] for k in sorted_humidity_sensor_ids if not humidity_sensors[k].get('disabled', False)]

    pressure_sensors = config['pressure_sensors']
    sorted_pressure_sensor_ids = sorted(pressure_sensors, key=lambda key: pressure_sensors[key]['display_order'])
    sorted_pressure_sensors = [pressure_sensors[k] for k in sorted_pressure_sensor_ids if not pressure_sensors[k].get('disabled', False)]

    lake_temp_sensors = config['lake_temp_sensors']
    sorted_lake_temp_sensor_ids = sorted(lake_temp_sensors, key=lambda key: lake_temp_sensors[key]['display_order'])
    sorted_lake_temp_sensors = [lake_temp_sensors[k] for k in sorted_lake_temp_sensor_ids if not lake_temp_sensors[k].get('disabled', False)]

    wind_speed_sensors = config['wind_speed_sensors']
    sorted_wind_speed_sensor_ids = sorted(wind_speed_sensors, key=lambda key: wind_speed_sensors[key]['display_order'])
    sorted_wind_speed_sensors = [wind_speed_sensors[k] for k in sorted_wind_speed_sensor_ids if not wind_speed_sensors[k].get('disabled', False)]


    graphs = [
        {
            'rrd_path': os.path.join(DIR, 'database', 'temp.rrd'),
            'vertical_label': 'Temperature (°F)',
            'unit': '°',
            'sensors': sorted_temp_sensors,
            'variations': [
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
            'rrd_path': os.path.join(DIR, 'database', 'pressure.rrd'),
            'vertical_label': 'Air Pressure (Inches)',
            'unit': '"',
            'sensors': sorted_pressure_sensors,
            'extra_options': [
                '--alt-autoscale',
                '--alt-y-grid',
            ],
            'variations': [
                {
                    'filename': 'pressure_daily.png',
                    'title': 'Air Pressure Last 24 Hours',
                    'start': '-1d'
                },
                {
                    'filename': 'pressure_daily_mobile.png',
                    'title': 'Air Pressure Last 24 Hours',
                    'start': '-1d',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'pressure_weekly.png',
                    'title': 'Weekly Air Pressure',
                    'start': '-1w'
                },
                {
                    'filename': 'pressure_weekly_mobile.png',
                    'title': 'Weekly Air Pressure',
                    'start': '-1w',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'pressure_monthly.png',
                    'title': 'Monthly Air Pressure',
                    'start': '-1m'
                },
                {
                    'filename': 'pressure_monthly_mobile.png',
                    'title': 'Monthly Air Pressure',
                    'start': '-1m',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'pressure_yearly.png',
                    'title': 'Yearly Air Pressure',
                    'start': '-1y'
                },
                {
                    'filename': 'pressure_yearly_mobile.png',
                    'title': 'Yearly Air Pressure',
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
                    'filename': 'lake_temp_daily.png',
                    'title': 'Lake Temperature Last 24 Hours',
                    'start': '-1d'
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
                },
                {
                    'filename': 'lake_temp_weekly.png',
                    'title': 'Weekly Lake Temperature',
                    'start': '-1w'
                },
                {
                    'filename': 'lake_temp_weekly_mobile.png',
                    'title': 'Weekly Lake Temperature',
                    'start': '-1w',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'lake_temp_monthly.png',
                    'title': 'Monthly Lake Temperature',
                    'start': '-1m'
                },
                {
                    'filename': 'lake_temp_monthly_mobile.png',
                    'title': 'Monthly Lake Temperature',
                    'start': '-1m',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'lake_temp_yearly.png',
                    'title': 'Yearly Lake Temperature',
                    'start': '-1y'
                },
                {
                    'filename': 'lake_temp_yearly_mobile.png',
                    'title': 'Yearly Lake Temperature',
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
            'rrd_path': os.path.join(DIR, 'database', 'wind_speed.rrd'),
            'vertical_label': 'Wind Speed (m/s)',
            'unit': ' ',
            'sensors': sorted_wind_speed_sensors,
            'variations': [
                {
                    'filename': 'wind_speed_daily.png',
                    'title': 'Wind Speed Last 24 Hours',
                    'start': '-1d'
                },
                {
                    'filename': 'wind_speed_daily_mobile.png',
                    'title': 'Wind Speed Last 24 Hours',
                    'start': '-1d',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'wind_speed_weekly.png',
                    'title': 'Weekly Wind Speed',
                    'start': '-1w'
                },
                {
                    'filename': 'wind_speed_weekly_mobile.png',
                    'title': 'Weekly Wind Speed',
                    'start': '-1w',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'wind_speed_monthly.png',
                    'title': 'Monthly Wind Speed',
                    'start': '-1m'
                },
                {
                    'filename': 'wind_speed_monthly_mobile.png',
                    'title': 'Monthly Wind Speed',
                    'start': '-1m',
                    'title_font': 30,
                    'axis_font': 17,
                    'legend_font': 29,
                    'unit_font': 20,
                    'padding': 4,
                    'line_stroke': 8
                },
                {
                    'filename': 'wind_speed_yearly.png',
                    'title': 'Yearly Wind Speed',
                    'start': '-1y'
                },
                {
                    'filename': 'wind_speed_yearly_mobile.png',
                    'title': 'Yearly Wind Speed',
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

    ]

    directory = os.path.join(DIR, 'latest_graphs')

    if not os.path.exists(directory):
        os.makedirs(directory)

    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    lake_temp_sensors_disabled = config.get('lake_temp_sensors_disabled', True)

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
                if lake_temp_sensors_disabled:
                    if 'lake' in graph_variation['filename'] or 'wind' in graph_variation['filename']:
                        continue
                if 'daily' in graph_variation['filename'] and not daily:
                    continue
                if 'yearly' in graph_variation['filename'] and not yearly:
                    continue
                if 'monthly' in graph_variation['filename'] and not monthly:
                    continue
                if 'weekly' in graph_variation['filename'] and not weekly:
                    continue
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

                site_display_name = config.get("site_display_name", False)
                graphs_with_no_display_name = ['lake', 'wind']
                if site_display_name and all(x not in graph['rrd_path'] for x in graphs_with_no_display_name):
                    graph_title = f"{site_display_name} {graph_variation['title']}"
                else:
                    graph_title = graph_variation['title']

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
                ''' % (directory, graph_variation['filename'], graph_title, \
                    graph_variation['title_font'], graph_variation['axis_font'], \
                    graph_variation['legend_font'], graph_variation['unit_font'], \
                    graph_variation['start'], graph['vertical_label'], \
                    label.rjust(len(label) + max_name_length))
                if 'extra_options' in graph:
                    for extra_option in graph['extra_options']:
                        command += ' %s ' % (extra_option)

                for sensor in graph['sensors']:
                    display_name = sensor['name'] + '\:'
                    
                    if graph['unit'] == '""':
                        command += '''DEF:%(ds_name)s=%(rrd_path)s:%(ds_name)s:AVERAGE \\
                            LINE%(line_stroke)d:%(ds_name)s%(color)s:'%(display_name)s' \\
                            GPRINT:%(ds_name)s:LAST:'%%%(padding)d.2lf%(unit)s' \\
                            GPRINT:%(ds_name)s:MIN:'%%%(padding)d.2lf%(unit)s' \\
                            GPRINT:%(ds_name)s:MAX:'%%%(padding)d.2lf%(unit)s' \\
                            GPRINT:%(ds_name)s:AVERAGE:'%%%(padding)d.2lf%(unit)s\\n' \\
                            ''' % {
                                    'ds_name': sensor['ds_name'],
                                    'rrd_path': graph['rrd_path'],
                                    'line_stroke': graph_variation['line_stroke'],
                                    'color': sensor['color'],
                                    'display_name': display_name.ljust(max_name_length),
                                    'padding': padding,
                                    'unit': graph['unit']
                                  }
                    else:
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
                    if config.get("daily_basement_heat_cost", False):
                        daily_basement_heat_minutes = temperature.getCurrentDailyHeatingMinutes(2)
                        daily_basement_heat_cost = round((daily_basement_heat_minutes / 60) * 4 * .17758, 2)
                        command += f"' | ${daily_basement_heat_cost:.2f} basement heat'"

                #print(command)
                tic = time.perf_counter()
                status = getstatusoutput(command)
                toc = time.perf_counter()
                print(f"{graph_variation['filename']} took {toc - tic:0.4f} seconds")

    overall_toc = time.perf_counter()
    print(f"Graph generation took {overall_toc - overall_tic:0.4f} seconds")

if __name__ == "__main__":
    createGraphs()
