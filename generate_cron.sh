#!/bin/bash

p=$(which python3)
x=$(pwd)/temps.py
l=$(pwd)/cron_log.txt
s=10

echo "*/$s * * * * $p $x >> $l 2>&1"
