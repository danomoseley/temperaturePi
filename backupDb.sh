#!/bin/bash

DIR=$(cd $(dirname $0); pwd -P)
RSYNC_BWLIMIT=500

rsync -a --bwlimit=$RSYNC_BWLIMIT $DIR/*.{db,rrd} dan@direct.danomoseley.com:/var/www/camp/

