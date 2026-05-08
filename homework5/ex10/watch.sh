#!/bin/bash


while true
do
for file in ~/watch/*
do

	if [ -f "$file" ] && [ "${file##*.}" != "back" ];then
		cat "$file"
		mv "$file" "$file.back"
	fi
done
sleep 2
done
