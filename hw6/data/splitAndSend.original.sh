#!/bin/bash

if [ -z "$1" ]; then
        echo "Missing output folder name"
        exit 1
fi

split -l 10000  orders.txt chunk 

for f in `ls chunk*`; do
        if [ "$2" == "local" ]; then
                mv $f $1
        else
                hadoop fs -put $f $1/
                rm -f $f
        fi
        sleep 3 
done
