#!/bin/bash

while getopts s: flag
do
    case "${flag}" in
        s) sensor=${OPTARG};;
    esac
done

if [[ $sensor == 'sentinel1b' ]]
then
    echo "Processing sensor: $sensor";
    source ./scripts/run_tests.sh
else
    echo "Argument not understood"
fi
