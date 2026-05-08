#!/bin/bash
FILE="config.txt" 

if [[ -f "$FILE" ]]; then
	echo "$FILE exists"
else 
	echo "$FILE doesn't exist"
fi
