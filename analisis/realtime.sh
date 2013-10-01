#!/bin/bash
pv -L 10k  -B 10 -q  | mawk -W interactive '{if (NF==3){print $1; fflush()}}' | ./procesar.py | feedgnuplot --stream  0 --lines --dataid --autolegend --xlen 1000  
