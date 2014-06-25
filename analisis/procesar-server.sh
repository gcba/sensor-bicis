#!/bin/bash

# Shell script to run the sensor processing code, plus add some logging every couple of seconds.
# writes every line received to /tmp/valores-sensors.csv, and outputs only detected bikes and 
# 10 seconds pressure readings to stdout (should be redirected to a log file)

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source ./bin/activate

if [ -z "$SENSOR_HOST" ]; then
    echo "Defina la variable \$SENSOR_HOST"
    exit 1;
fi

nc -v -d $SENSOR_HOST 54321 \
| awk '( (NR > 100) && (NF == 3) && ($0 !~ /[A-Za-z]/)  ) { print }' \
| ./procesar.py \
| awk '{ if ((NR % 1000000)==0 || $0 ~ /bici/ ){ print $0;}}'

