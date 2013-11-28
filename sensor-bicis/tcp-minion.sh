#!/bin/bash
socat tcp-l:54321,fork,reuseaddr open:/dev/ttyACM0,raw,nonblock,waitlock=/tmp/acm0.lock,echo=0,b38400,crnl
