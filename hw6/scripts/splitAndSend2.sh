#!/bin/bash

# Split data into chunks
split -l 10000 /home/tim/e63-coursework/hw6/data/orders.txt /home/tim/e63-coursework/hw6/data/staging/chunk

# Simulate stream with 3 seconds difference
for f in `ls /home/tim/e63-coursework/hw6/data/staging/chunk*`; do
        sleep 3
        mv $f /home/tim/e63-coursework/hw6/data/input/
        rm -f $f
done