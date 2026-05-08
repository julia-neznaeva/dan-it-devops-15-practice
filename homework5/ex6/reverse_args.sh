#!/bin/bash

args=("$@")
COUNTER=$#
RESULT=""

while [ $COUNTER -ge 0 ]
do
	RESULT="$RESULT ${args[$COUNTER]}"
	COUNTER=$((COUNTER-1)) 
done

echo "$RESULT"
