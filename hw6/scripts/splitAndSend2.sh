#!/bin/bash

split -l 10000 /home/tim/e63-coursework/hw6/data/orders.txt chunk

for f in `ls chunk*`; do
        mv $f /home/tim/e63-coursework/hw6/data/staging
        sleep 3 
        mv /home/tim/e63-coursework/hw6/data/staging/$f /home/tim/e63-coursework/hw6/data/input
        rm -f $f
done
