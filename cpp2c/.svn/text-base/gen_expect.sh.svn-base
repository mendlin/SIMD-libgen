#!/bin/bash
BASE_EXEC=./cpp2c.rb
FILES=test_data/*

echo "--------------Generating expected output----------------"
for f in $FILES
do
	filename=$(basename "$f")
	echo "Processing $f file..."
	$BASE_EXEC $f -o "expected_output/$filename"
done
