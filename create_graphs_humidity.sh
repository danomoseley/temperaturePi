#!/bin/bash
DIR=$(cd $(dirname $0); pwd -P)

rrdtool graph $DIR/latest_graphs/humidity_hourly.png \
-w 1024 -h 500 -a PNG \
--title='Humidity Last 4 Hours' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--start -14400 --end now \
--vertical-label "Relative Humidity (%)" \
COMMENT:"                               CURRENT     MIN         MAX      AVERAGE\n" \
DEF:living_room=$DIR/humidity.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf%%" \
GPRINT:living_room:MIN:"    %2.1lf%%" \
GPRINT:living_room:MAX:"    %2.1lf%%" \
GPRINT:living_room:AVERAGE:"    %2.1lf%%\n" \

#daily
rrdtool graph $DIR/latest_graphs/humidity_daily.png --start -1d \
-w 1024 -h 500 -a PNG \
--title='Humidity Last 24 Hours' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Relative Humidity (%)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/humidity.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf%%" \
GPRINT:living_room:MIN:"    %2.1lf%%" \
GPRINT:living_room:MAX:"    %2.1lf%%" \
GPRINT:living_room:AVERAGE:"    %2.1lf%%\n" \

#daily mobile
rrdtool graph $DIR/latest_graphs/humidity_daily_mobile.png --start -1d \
-w 1024 -h 500 -a PNG \
--title='Camp Humidity Last 24 Hours' \
--font TITLE:30: \
--font AXIS:17: \
--font LEGEND:30: \
--font UNIT:20: \
--slope-mode \
--vertical-label "Relative Humidity (%)" \
COMMENT:"                 NOW     MIN    MAX     AVG\n" \
DEF:living_room=$DIR/humidity.rrd:living_room:AVERAGE \
LINE8:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"%2.1lf%%" \
GPRINT:living_room:MIN:"%2.1lf%%" \
GPRINT:living_room:MAX:"%2.1lf%%" \
GPRINT:living_room:AVERAGE:"%2.1lf%%\n" \
"COMMENT:\n" \
"COMMENT:$(date "+%m/%d %l:%M %p" | sed 's/:/\\:/g')" \

#weekly
rrdtool graph $DIR/latest_graphs/humidity_weekly.png --start -1w \
-w 1024 -h 500 -a PNG \
--title='Weekly Humidity' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Relative Humidity (%)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/humidity.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf%%" \
GPRINT:living_room:MIN:"    %2.1lf%%" \
GPRINT:living_room:MAX:"    %2.1lf%%" \
GPRINT:living_room:AVERAGE:"    %2.1lf%%\n" \

#monthly
rrdtool graph $DIR/latest_graphs/humidity_monthly.png --start -1m \
-w 1024 -h 500 -a PNG \
--title='Monthly Humidity' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Relative Humidity (%)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/humidity.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf%%" \
GPRINT:living_room:MIN:"    %2.1lf%%" \
GPRINT:living_room:MAX:"    %2.1lf%%" \
GPRINT:living_room:AVERAGE:"    %2.1lf%%\n" \

#yearly
rrdtool graph $DIR/latest_graphs/humidity_yearly.png --start -1y \
-w 1024 -h 500 -a PNG \
--title='Yearly Humidity' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Relative Humidity (%)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/humidity.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf%%" \
GPRINT:living_room:MIN:"    %2.1lf%%" \
GPRINT:living_room:MAX:"    %2.1lf%%" \
GPRINT:living_room:AVERAGE:"    %2.1lf%%\n" \
