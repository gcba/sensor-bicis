#!/bin/bash

# Shell script to run the sensor processing code, plus add some logging every couple of seconds.
# writes every line received to /tmp/valores-sensors.csv, and outputs only detected bikes and 
# 10 seconds pressure readings to stdout (should be redirected to a log file)

nc -d $SENSOR_HOST 54321 \
| awk '( (NR > 100) && (NF == 3) && ($0 !~ /[A-Za-z]/)  ) { print }' \
| tee -a /tmp/valores-sensor.csv \
| ./procesar.py \
| awk '{ if ((NR % 1000000)==0 || $0 ~ /bici/ ){ print $0;}}'

