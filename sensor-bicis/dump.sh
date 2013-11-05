#!/bin/bash
set -v
stty -F /dev/ttyACM0 cs8 38400 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts
< /dev/ttyACM0 awk '( (NR > 100) && (NF == 3) && ($0 !~ /[A-Za-z]/)  ) { print }'
