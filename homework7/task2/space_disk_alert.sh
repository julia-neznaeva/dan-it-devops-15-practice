#!/bin/bash

USAGE=$(df / | awk 'NR==2 {gsub("%",""); print $5}')

echo "$THRESHOLD"

if [ "$USAGE" -gt "$THRESHOLD" ]; then
	echo "Disk usage high" >> /var/log/disk.log
fi

