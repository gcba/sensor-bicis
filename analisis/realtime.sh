#!/bin/bash
pv -L 10k  -B 10 -q  | awk '{if (NF==3){print $1; fflush()}}' | ./procesar.py | feedgnuplot --stream  0 --lines --dataid --autolegend --xlen 10000 --points 2
