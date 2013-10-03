#!/bin/bash
mawk -W interactive '/[^a-zA-Z]/ {if (NF==3){print $1; fflush()}}' | ./procesar.py | feedgnuplot --stream  1 --lines --dataid --autolegend -xlen 5000  
