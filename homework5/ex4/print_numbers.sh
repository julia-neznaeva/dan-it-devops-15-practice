#!/bin/bash

COUNTER=1

while [ "$COUNTER" -le 10 ]
do
	echo "$COUNTER"
	COUNTER=$((COUNTER+1))
done
