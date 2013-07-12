#!/bin/bash
BASE_EXEC=./cpp2c.rb
FILES=test_data/*

rm -rf output
mkdir output

echo "--------------Generating output----------------"
for f in $FILES
do
	filename=$(basename "$f")
	echo "Processing $f file..."
	$BASE_EXEC $f -o "output/$filename"
done

echo "--------------Diff result----------------------"
for f in $FILES
do
	filename=$(basename "$f")
	echo "Diff result of $filename file..."
	diff "expected_output/$filename" "output/$filename"
done