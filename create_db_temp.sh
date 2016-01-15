#!/bin/bash
rrdtool create temp.rrd --start N --step 300 \
DS:bedroom:GAUGE:600:U:U \
DS:under_stairs:GAUGE:600:U:U \
DS:north_cellar:GAUGE:600:U:U \
DS:outside:GAUGE:600:U:U \
DS:living_room:GAUGE:600:U:U \
RRA:AVERAGE:0.5:1:12 \
RRA:AVERAGE:0.5:1:288 \
RRA:AVERAGE:0.5:12:168 \
RRA:AVERAGE:0.5:12:720 \
RRA:AVERAGE:0.5:288:365
