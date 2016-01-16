#!/bin/bash
DIR=$(cd $(dirname $0); pwd -P)

rrdtool graph $DIR/latest_graphs/temp_hourly.png \
-w 1024 -h 500 -a PNG \
--title='Temperature Last 4 Hours' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--start -14400 --end now \
--vertical-label "Temperature (°F)" \
COMMENT:"                               CURRENT     MIN         MAX      AVERAGE\n" \
DEF:living_room=$DIR/temp.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf°" \
GPRINT:living_room:MIN:"    %2.1lf°" \
GPRINT:living_room:MAX:"    %2.1lf°" \
GPRINT:living_room:AVERAGE:"    %2.1lf°\n" \
DEF:bedroom=$DIR/temp.rrd:bedroom:AVERAGE \
LINE2:bedroom#0033CC:"Bedroom By Rory's Cage\:" \
GPRINT:bedroom:LAST:"    %2.1lf°" \
GPRINT:bedroom:MIN:"    %2.1lf°" \
GPRINT:bedroom:MAX:"    %2.1lf°" \
GPRINT:bedroom:AVERAGE:"    %2.1lf°\n" \
DEF:kitchen_sink=$DIR/temp.rrd:kitchen_sink:AVERAGE \
LINE2:kitchen_sink#fdd80e:"Kitchen Sink\:" \
GPRINT:kitchen_sink:LAST:"              %2.1lf°" \
GPRINT:kitchen_sink:MIN:"    %2.1lf°" \
GPRINT:kitchen_sink:MAX:"    %2.1lf°" \
GPRINT:kitchen_sink:AVERAGE:"    %2.1lf°\n" \
DEF:north_cellar=$DIR/temp.rrd:north_cellar:AVERAGE \
LINE2:north_cellar#CC00CC:"Cellar Northwest Corner\:" \
GPRINT:north_cellar:LAST:"   %2.1lf°" \
GPRINT:north_cellar:MIN:"    %2.1lf°" \
GPRINT:north_cellar:MAX:"    %2.1lf°" \
GPRINT:north_cellar:AVERAGE:"    %2.1lf°\n" \
DEF:under_stairs=$DIR/temp.rrd:under_stairs:AVERAGE \
LINE2:under_stairs#009900:"Under Stairs by Well Pipe\:" \
GPRINT:under_stairs:LAST:" %2.1lf°" \
GPRINT:under_stairs:MIN:"    %2.1lf°" \
GPRINT:under_stairs:MAX:"    %2.1lf°" \
GPRINT:under_stairs:AVERAGE:"    %2.1lf°\n" \
DEF:outside=$DIR/temp.rrd:outside:AVERAGE \
LINE2:outside#CC0000:"Outside Southwest Corner\:" \
GPRINT:outside:LAST:"  %2.1lf°" \
GPRINT:outside:MIN:"    %2.1lf°" \
GPRINT:outside:MAX:"    %2.1lf°" \
GPRINT:outside:AVERAGE:"    %2.1lf°\n" \

#daily
rrdtool graph $DIR/latest_graphs/temp_daily.png --start -1d \
-w 1024 -h 500 -a PNG \
--title='Temperature Last 24 Hours' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Temperature (°F)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/temp.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf°" \
GPRINT:living_room:MIN:"    %2.1lf°" \
GPRINT:living_room:MAX:"    %2.1lf°" \
GPRINT:living_room:AVERAGE:"    %2.1lf°\n" \
DEF:bedroom=$DIR/temp.rrd:bedroom:AVERAGE \
LINE2:bedroom#0033CC:"Bedroom By Rory's Cage\:" \
GPRINT:bedroom:LAST:"    %2.1lf°" \
GPRINT:bedroom:MIN:"    %2.1lf°" \
GPRINT:bedroom:MAX:"    %2.1lf°" \
GPRINT:bedroom:AVERAGE:"    %2.1lf°\n" \
DEF:kitchen_sink=$DIR/temp.rrd:kitchen_sink:AVERAGE \
LINE2:kitchen_sink#fdd80e:"Kitchen Sink\:" \
GPRINT:kitchen_sink:LAST:"              %2.1lf°" \
GPRINT:kitchen_sink:MIN:"    %2.1lf°" \
GPRINT:kitchen_sink:MAX:"    %2.1lf°" \
GPRINT:kitchen_sink:AVERAGE:"    %2.1lf°\n" \
DEF:north_cellar=$DIR/temp.rrd:north_cellar:AVERAGE \
LINE2:north_cellar#CC00CC:"Cellar Northwest Corner\:" \
GPRINT:north_cellar:LAST:"   %2.1lf°" \
GPRINT:north_cellar:MIN:"    %2.1lf°" \
GPRINT:north_cellar:MAX:"    %2.1lf°" \
GPRINT:north_cellar:AVERAGE:"    %2.1lf°\n" \
DEF:under_stairs=$DIR/temp.rrd:under_stairs:AVERAGE \
LINE2:under_stairs#009900:"Under Stairs by Well Pipe\:" \
GPRINT:under_stairs:LAST:" %2.1lf°" \
GPRINT:under_stairs:MIN:"    %2.1lf°" \
GPRINT:under_stairs:MAX:"    %2.1lf°" \
GPRINT:under_stairs:AVERAGE:"    %2.1lf°\n" \
DEF:outside=$DIR/temp.rrd:outside:AVERAGE \
LINE2:outside#CC0000:"Outside Southwest Corner\:" \
GPRINT:outside:LAST:"  %2.1lf°" \
GPRINT:outside:MIN:"    %2.1lf°" \
GPRINT:outside:MAX:"    %2.1lf°" \
GPRINT:outside:AVERAGE:"    %2.1lf°\n" \

#daily mobile
rrdtool graph $DIR/latest_graphs/temp_daily_mobile.png --start -1d \
-w 1024 -h 500 -a PNG \
--title='Camp Temperature Last 24 Hours' \
--font TITLE:30: \
--font AXIS:17: \
--font LEGEND:30: \
--font UNIT:20: \
--slope-mode \
--vertical-label "Temperature (°F)" \
COMMENT:"                 NOW     MIN    MAX     AVG\n" \
DEF:living_room=$DIR/temp.rrd:living_room:AVERAGE \
LINE8:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"%2.1lf°" \
GPRINT:living_room:MIN:"%2.1lf°" \
GPRINT:living_room:MAX:"%2.1lf°" \
GPRINT:living_room:AVERAGE:"%2.1lf°\n" \
DEF:bedroom=$DIR/temp.rrd:bedroom:AVERAGE \
LINE8:bedroom#0033CC:"Bedroom\:" \
GPRINT:bedroom:LAST:"    %2.1lf°" \
GPRINT:bedroom:MIN:"%2.1lf°" \
GPRINT:bedroom:MAX:"%2.1lf°" \
GPRINT:bedroom:AVERAGE:"%2.1lf°\n" \
DEF:kitchen_sink=$DIR/temp.rrd:kitchen_sink:AVERAGE \
LINE8:kitchen_sink#fdd80e:"Kitch Sink\:" \
GPRINT:kitchen_sink:LAST:" %2.1lf°" \
GPRINT:kitchen_sink:MIN:"%2.1lf°" \
GPRINT:kitchen_sink:MAX:"%2.1lf°" \
GPRINT:kitchen_sink:AVERAGE:"%2.1lf°\n" \
DEF:north_cellar=$DIR/temp.rrd:north_cellar:AVERAGE \
LINE8:north_cellar#CC00CC:"Cellar\:" \
GPRINT:north_cellar:LAST:"     %2.1lf°" \
GPRINT:north_cellar:MIN:"%2.1lf°" \
GPRINT:north_cellar:MAX:"%2.1lf°" \
GPRINT:north_cellar:AVERAGE:"%2.1lf°\n" \
DEF:under_stairs=$DIR/temp.rrd:under_stairs:AVERAGE \
LINE8:under_stairs#009900:"Well Pipe\:" \
GPRINT:under_stairs:LAST:"  %2.1lf°" \
GPRINT:under_stairs:MIN:"%2.1lf°" \
GPRINT:under_stairs:MAX:"%2.1lf°" \
GPRINT:under_stairs:AVERAGE:"%2.1lf°\n" \
DEF:outside=$DIR/temp.rrd:outside:AVERAGE \
LINE8:outside#CC0000:"Outside\:" \
GPRINT:outside:LAST:"    %2.1lf°" \
GPRINT:outside:MIN:"%2.1lf°" \
GPRINT:outside:MAX:"%2.1lf°" \
GPRINT:outside:AVERAGE:"%2.1lf°\n" \
"COMMENT:\n" \
"COMMENT:$(date "+%m/%d %l:%M %p" | sed 's/:/\\:/g')" \

#weekly
rrdtool graph $DIR/latest_graphs/temp_weekly.png --start -1w \
-w 1024 -h 500 -a PNG \
--title='Weekly Temperature' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Temperature (°F)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/temp.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf°" \
GPRINT:living_room:MIN:"    %2.1lf°" \
GPRINT:living_room:MAX:"    %2.1lf°" \
GPRINT:living_room:AVERAGE:"    %2.1lf°\n" \
DEF:bedroom=$DIR/temp.rrd:bedroom:AVERAGE \
LINE2:bedroom#0033CC:"Bedroom By Rory's Cage\:" \
GPRINT:bedroom:LAST:"    %2.1lf°" \
GPRINT:bedroom:MIN:"    %2.1lf°" \
GPRINT:bedroom:MAX:"    %2.1lf°" \
GPRINT:bedroom:AVERAGE:"    %2.1lf°\n" \
DEF:kitchen_sink=$DIR/temp.rrd:kitchen_sink:AVERAGE \
LINE2:kitchen_sink#fdd80e:"Kitchen Sink\:" \
GPRINT:kitchen_sink:LAST:"              %2.1lf°" \
GPRINT:kitchen_sink:MIN:"    %2.1lf°" \
GPRINT:kitchen_sink:MAX:"    %2.1lf°" \
GPRINT:kitchen_sink:AVERAGE:"    %2.1lf°\n" \
DEF:north_cellar=$DIR/temp.rrd:north_cellar:AVERAGE \
LINE2:north_cellar#CC00CC:"Cellar Northwest Corner\:" \
GPRINT:north_cellar:LAST:"   %2.1lf°" \
GPRINT:north_cellar:MIN:"    %2.1lf°" \
GPRINT:north_cellar:MAX:"    %2.1lf°" \
GPRINT:north_cellar:AVERAGE:"    %2.1lf°\n" \
DEF:under_stairs=$DIR/temp.rrd:under_stairs:AVERAGE \
LINE2:under_stairs#009900:"Under Stairs by Well Pipe\:" \
GPRINT:under_stairs:LAST:" %2.1lf°" \
GPRINT:under_stairs:MIN:"    %2.1lf°" \
GPRINT:under_stairs:MAX:"    %2.1lf°" \
GPRINT:under_stairs:AVERAGE:"    %2.1lf°\n" \
DEF:outside=$DIR/temp.rrd:outside:AVERAGE \
LINE2:outside#CC0000:"Outside Southwest Corner\:" \
GPRINT:outside:LAST:"  %2.1lf°" \
GPRINT:outside:MIN:"    %2.1lf°" \
GPRINT:outside:MAX:"    %2.1lf°" \
GPRINT:outside:AVERAGE:"    %2.1lf°\n" \

#monthly
rrdtool graph $DIR/latest_graphs/temp_monthly.png --start -1m \
-w 1024 -h 500 -a PNG \
--title='Monthly Temperature' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Temperature (°F)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/temp.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf°" \
GPRINT:living_room:MIN:"    %2.1lf°" \
GPRINT:living_room:MAX:"    %2.1lf°" \
GPRINT:living_room:AVERAGE:"    %2.1lf°\n" \
DEF:bedroom=$DIR/temp.rrd:bedroom:AVERAGE \
LINE2:bedroom#0033CC:"Bedroom By Rory's Cage\:" \
GPRINT:bedroom:LAST:"    %2.1lf°" \
GPRINT:bedroom:MIN:"    %2.1lf°" \
GPRINT:bedroom:MAX:"    %2.1lf°" \
GPRINT:bedroom:AVERAGE:"    %2.1lf°\n" \
DEF:kitchen_sink=$DIR/temp.rrd:kitchen_sink:AVERAGE \
LINE2:kitchen_sink#fdd80e:"Kitchen Sink\:" \
GPRINT:kitchen_sink:LAST:"              %2.1lf°" \
GPRINT:kitchen_sink:MIN:"    %2.1lf°" \
GPRINT:kitchen_sink:MAX:"    %2.1lf°" \
GPRINT:kitchen_sink:AVERAGE:"    %2.1lf°\n" \
DEF:north_cellar=$DIR/temp.rrd:north_cellar:AVERAGE \
LINE2:north_cellar#CC00CC:"Cellar Northwest Corner\:" \
GPRINT:north_cellar:LAST:"   %2.1lf°" \
GPRINT:north_cellar:MIN:"    %2.1lf°" \
GPRINT:north_cellar:MAX:"    %2.1lf°" \
GPRINT:north_cellar:AVERAGE:"    %2.1lf°\n" \
DEF:under_stairs=$DIR/temp.rrd:under_stairs:AVERAGE \
LINE2:under_stairs#009900:"Under Stairs by Well Pipe\:" \
GPRINT:under_stairs:LAST:" %2.1lf°" \
GPRINT:under_stairs:MIN:"    %2.1lf°" \
GPRINT:under_stairs:MAX:"    %2.1lf°" \
GPRINT:under_stairs:AVERAGE:"    %2.1lf°\n" \
DEF:outside=$DIR/temp.rrd:outside:AVERAGE \
LINE2:outside#CC0000:"Outside Southwest Corner\:" \
GPRINT:outside:LAST:"  %2.1lf°" \
GPRINT:outside:MIN:"    %2.1lf°" \
GPRINT:outside:MAX:"    %2.1lf°" \
GPRINT:outside:AVERAGE:"    %2.1lf°\n" \

#yearly
rrdtool graph $DIR/latest_graphs/temp_yearly.png --start -1y \
-w 1024 -h 500 -a PNG \
--title='Yearly Temperature' \
--font TITLE:12: \
--font AXIS:8: \
--font LEGEND:10: \
--font UNIT:8: \
--slope-mode \
--vertical-label "Temperature (°F)" \
COMMENT:"                               CURRENT      MIN        MAX       AVERAGE\n" \
DEF:living_room=$DIR/temp.rrd:living_room:AVERAGE \
LINE2:living_room#66CCFF:"Living Room\:" \
GPRINT:living_room:LAST:"               %2.1lf°" \
GPRINT:living_room:MIN:"    %2.1lf°" \
GPRINT:living_room:MAX:"    %2.1lf°" \
GPRINT:living_room:AVERAGE:"    %2.1lf°\n" \
DEF:bedroom=$DIR/temp.rrd:bedroom:AVERAGE \
LINE2:bedroom#0033CC:"Bedroom By Rory's Cage\:" \
GPRINT:bedroom:LAST:"    %2.1lf°" \
GPRINT:bedroom:MIN:"    %2.1lf°" \
GPRINT:bedroom:MAX:"    %2.1lf°" \
GPRINT:bedroom:AVERAGE:"    %2.1lf°\n" \
DEF:kitchen_sink=$DIR/temp.rrd:kitchen_sink:AVERAGE \
LINE2:kitchen_sink#fdd80e:"Kitchen Sink\:" \
GPRINT:kitchen_sink:LAST:"              %2.1lf°" \
GPRINT:kitchen_sink:MIN:"    %2.1lf°" \
GPRINT:kitchen_sink:MAX:"    %2.1lf°" \
GPRINT:kitchen_sink:AVERAGE:"    %2.1lf°\n" \
DEF:north_cellar=$DIR/temp.rrd:north_cellar:AVERAGE \
LINE2:north_cellar#CC00CC:"Cellar Northwest Corner\:" \
GPRINT:north_cellar:LAST:"   %2.1lf°" \
GPRINT:north_cellar:MIN:"    %2.1lf°" \
GPRINT:north_cellar:MAX:"    %2.1lf°" \
GPRINT:north_cellar:AVERAGE:"    %2.1lf°\n" \
DEF:under_stairs=$DIR/temp.rrd:under_stairs:AVERAGE \
LINE2:under_stairs#009900:"Under Stairs by Well Pipe\:" \
GPRINT:under_stairs:LAST:" %2.1lf°" \
GPRINT:under_stairs:MIN:"    %2.1lf°" \
GPRINT:under_stairs:MAX:"    %2.1lf°" \
GPRINT:under_stairs:AVERAGE:"    %2.1lf°\n" \
DEF:outside=$DIR/temp.rrd:outside:AVERAGE \
LINE2:outside#CC0000:"Outside Southwest Corner\:" \
GPRINT:outside:LAST:"  %2.1lf°" \
GPRINT:outside:MIN:"    %2.1lf°" \
GPRINT:outside:MAX:"    %2.1lf°" \
GPRINT:outside:AVERAGE:"    %2.1lf°\n" \

