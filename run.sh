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
    source ./scripts/process_sentinel1b.sh
elif [[ $sensor == 'alos2palsar2' ]]
then
    echo "Processing sensor: $sensor";

elif [[ $sensor == 'landsat8' ]]
then 
    echo "Processing sensor: $sensor";

elif [[ $sensor == 'sentinel2' ]]
then
    echo "Processing sensor: $sensor";

else
    echo "Sensor argument not understood"
fi
