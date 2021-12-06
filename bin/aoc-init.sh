#!/usr/bin/env bash

YEAR=$(date +%Y)
DAY=$(date +%d)

BASE_DIR=$(dirname $(dirname $0))

PUZZLE_PATH=$BASE_DIR/$YEAR/$DAY.py

if [ -f $PUZZLE_PATH ]
then
	echo "$DAY.py already exists in $BASE_DIR/$YEAR"
else
	echo "Initializing $DAY.py in $BASE_DIR/$YEAR"
	cp $BASE_DIR/template.py $PUZZLE_PATH
fi
