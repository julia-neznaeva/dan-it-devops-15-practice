#!/bin/bash

LINES=$(wc -l < "$1")

echo "$1 has $LINES lines"
