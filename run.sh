#!/bin/bash

while getopts "s:a:e:l:p:d:b:" flag
do
    case "${flag}" in
        s) sensor=$OPTARG;;
        a) algorithm=$OPTARG;; 
        e) event=$OPTARG;;
        l) location=$OPTARG;;
    	p) povinc=$OPTARG;;
        d) dem=$OPTARG;;
        b) bounds=$OPTARG;;
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

BOUNDS="./data/${bounds}"
if [[ $sensor == 'sentinel1b' ]]
then
    INPUT="./data/SENTINEL1B"
    DEM="./data/${dem}"
    OUTPUT="./data/OUTPUT"
    echo "Processing sensor: $sensor";
    docker run \
            -v ./src/sentinel1b/:/function/src \
            -v ./shared/:/function/src/shared \
            -v ./data/:/function/src/data \
            -w /function/src \
            --env SENSOR="$sensor" \
            --env INPUT_DIR="$INPUT" \
            --env BOUNDS="$BOUNDS" \
            --env DEM="$DEM" \
            --env OUTPUT="$OUTPUT" \
            --env DB_PATH="$DB_PATH" \
            --env EVENT="$event" \
            --env LOCATION="$location" \
            -it aoi-sentinel1b python main.py
    source ./scripts/process_sentinel1b.sh $INPUT $BOUNDS $DEM $OUTPUT $DB_PATH $event $location
elif [[ $sensor == 'alos2palsar2' ]]
then
    INPUT="./data/ALOS2PALSAR2"
    OUTPUT="./data/OUTPUT"
    echo "Processing sensor: $sensor";
    docker run \
            -v ./src/alos2palsar2/:/function/src \
            -v ./shared/:/function/src/shared \
            -v ./data:/function/src/data \
            -w /function/src \
            --env SENSOR="$sensor" \
            --env INPUT_DIR="$INPUT" \
            --env OUTPUT="$OUTPUT" \
            --env DB_PATH="$DB_PATH" \
            --env EVENT="$event" \
            --env LOCATION="$location" \
            -it aoi-alos2palsar2 python3 main.py
    echo "Executing impact assesssment using ${povinc} column in the ${BOUNDS} dataset";
    docker run \
            -v ./src/impact-assessment/:/function/src \
            -v ./shared/:/function/src/shared \
            -v ./data:/function/src/data \
            -w /function/src \
            --env SENSOR="$sensor" \
            --env BOUNDS="$BOUNDS" \
            --env DB_PATH="$DB_PATH" \
            --env OUTPUT="$OUTPUT" \
            --env EVENT="$event" \
            --env LOCATION="$location" \
	        --env POVERTY_INCIDENCE="$povinc" \
            -it aoi-impact python3 main.py
elif [[ $sensor == 'landsat8' ]]
then 
    if [[ $algorithm == 'ndwi' ]]
    then
        INPUT="./data/LANDSAT8"
        OUTPUT="./data/OUTPUT"
        echo "Processing $algorithm for sensor: $sensor";
        source ./scripts/process_optical.sh $sensor $algorithm $INPUT $OUTPUT $DB_PATH $event $location
        echo "Executing impact assesssment using ${povinc} column in the ${BOUNDS} dataset";
        source ./scripts/impact_assessment.sh $sensor $BOUNDS $DB_PATH $OUTPUT $event $location $povinc
    elif [[ $algorithm == 'truecolor' ]]
    then
        INPUT="./data/LANDSAT8"
        OUTPUT="./data/OUTPUT"
        echo "Processing $algorithm for sensor: $sensor";
        source ./scripts/process_optical.sh $sensor $algorithm $INPUT $OUTPUT $DB_PATH $event $location
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
        docker run \
                -v ./src/optical/:/function/src \
                -v ./shared/:/function/src/shared \
                -v ./data:/function/src/data \
                -w /function/src \
                --env SENSOR="$sensor" \
                --env ALGORITHM="$algorithm" \
                --env INPUT="$INPUT" \
                --env OUTPUT="$OUTPUT" \
                --env DB_PATH="$DB_PATH" \
                --env EVENT="$event" \
                --env LOCATION="$location" \
                -it aoi-optical python3 main.py
        echo "Executing impact assesssment using ${povinc} column in the ${BOUNDS} dataset";
        docker run \
                -v ./src/impact-assessment/:/function/src \
                -v ./shared/:/function/src/shared \
                -v ./data:/function/src/data \
                -w /function/src \
                --env SENSOR="$sensor" \
                --env BOUNDS="$BOUNDS" \
                --env DB_PATH="$DB_PATH" \
                --env OUTPUT="$OUTPUT" \
                --env EVENT="$event" \
                --env LOCATION="$location" \
                --env POVERTY_INCIDENCE="$povinc" \
                -it aoi-impact python3 main.py
    elif [[ $algorithm == 'truecolor' ]]
    then
        INPUT="./data/SENTINEL2"
        OUTPUT="./data/OUTPUT"
        echo "Processing $algorithm for sensor: $sensor";
        docker run \
                -v ./src/optical/:/function/src \
                -v ./shared/:/function/src/shared \
                -v ./data:/function/src/data \
                -w /function/src \
                --env SENSOR="$sensor" \
                --env ALGORITHM="$algorithm" \
                --env INPUT="$INPUT" \
                --env OUTPUT="$OUTPUT" \
                --env DB_PATH="$DB_PATH" \
                --env EVENT="$event" \
                --env LOCATION="$location" \
                -it aoi-optical python3 main.py
        # source ./scripts/process_optical.sh $sensor $algorithm $INPUT $OUTPUT $DB_PATH $event $location
    else
        echo "Algorithm argument not understood"
    fi
else
    echo "Sensor argument not understood"
fi

echo "Pruning stopped containers..."
docker system prune -f
