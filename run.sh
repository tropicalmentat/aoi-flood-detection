#!/bin/bash

while getopts "s:a:" flag
do
    case "${flag}" in
        s) sensor=$OPTARG;;
        a) algorithm=$OPTARG;; 
    esac
done

DB_PATH="./data/source.db"
echo "Initializing database"
# check if database exists in path
if ! [ -f $DB_PATH ];
then
    echo "Database does not exist, initializing..."
    source ./scripts/init_database.sh
else
    echo "Database exists! Moving on..."
fi

if [[ $sensor == 'sentinel1b' ]]
then
    INPUT="./data/SENTINEL1B"
    BOUNDS="./data/National_PopAHS_PSA_2020.shp"
    DEM="./data/N00E120.zip"
    OUTPUT="./data/OUTPUT"
    echo "Processing sensor: $sensor";
    source ./scripts/process_sentinel1b.sh $INPUT $BOUNDS $DEM $OUTPUT
elif [[ $sensor == 'alos2palsar2' ]]
then
    INPUT="./data/ALOS2PALSAR2"
    OUTPUT="./data/OUTPUT"
    echo "Processing sensor: $sensor";
    source ./scripts/process_alos2palsar2.sh $INPUT $OUTPUT
elif [[ $sensor == 'landsat8' ]]
then 
    if [[ $algorithm == 'ndwi' ]]
    then
        INPUT="./data/LANDSAT8"
        OUTPUT="./data/OUTPUT"
        echo "Processing $algorithm for sensor: $sensor";
        source ./scripts/process_optical.sh $sensor $algorithm $INPUT $OUTPUT
    elif [[ $algorithm == 'truecolor' ]]
    then
        INPUT="./data/LANDSAT8"
        OUTPUT="./data/OUTPUT"
        echo "Processing $algorithm for sensor: $sensor";
        source ./scripts/process_optical.sh $sensor $algorithm $INPUT $OUTPUT
    else
        echo "Algorithm argument not understood"
    fi

elif [[ $sensor == 'sentinel2' ]]
then
    if [[ $algorithm == 'ndwi' ]]
    then
        INPUT="./data/SENTINEL2"
        OUTPUT="./data/OUTPUT"
        echo "Processing $algorithm for sensor: $sensor";
        source ./scripts/process_optical.sh $sensor $algorithm $INPUT $OUTPUT
    elif [[ $algorithm == 'truecolor' ]]
    then
        INPUT="./data/SENTINEL2"
        OUTPUT="./data/OUTPUT"
        echo "Processing $algorithm for sensor: $sensor";
        source ./scripts/process_optical.sh $sensor $algorithm $INPUT $OUTPUT
    else
        echo "Algorithm argument not understood"
    fi
else
    echo "Sensor argument not understood"
fi

