#!/bin/bash
# recibe el output de procesar.py y lo plotea
feedgnuplot --lines --domain --dataid \
   --legend 0 medicion \
   --legend 1 desvio \
   --legend 2 pulso  \
   --legend 3 bici \
   --ymin 10 --ymax 70 --timefmt '%m-%d %H:%M:%S'  \
   --curvestyle 2 "with points" \
   --curvestyle 3 "with points" \
   --extracmds 'set format x "%d-%H:%M:%S"'
