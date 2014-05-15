#!/bin/bash

while read -s -p ">" -n 1 ; do 
    fecha=`date +"%y-%m-%d %H:%M:%S.%3N"`
    echo $fecha	$REPLY
done
