#!/bin/bash

while getopts s: flag
do
    case "${flag}" in
        s) sensor=${OPTARG};;
    esac
done

if [[ $sensor == 'sentinel1b' ]]
then
    INPUT="./data/SENTINEL1B"
    BOUNDS="./data/National_PopAHS_PSA_2020.shp"
    DEM="./data/N00E120.zip"
    echo "Processing sensor: $sensor";
    source ./scripts/process_sentinel1b.sh $INPUT $BOUNDS $DEM
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
