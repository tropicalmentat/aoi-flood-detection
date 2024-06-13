#!/bin/bash

docker run \
        -v ./src/sentinel1b/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data/:/function/src/data \
        -w /function/src \
        --env SENSOR=sentinel1b \
        --env INPUT_DIR="$1" \
        --env BOUNDS="$2" \
        --env DEM="$3" \
        --env OUTPUT="$4" \
        --env DB_PATH="$5" \
        --env EVENT="$6" \
        --env LOCATION="$7" \
        -it aoi-sentinel1b python main.py