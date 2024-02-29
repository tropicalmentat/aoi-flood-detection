#!/bin/bash

# echo $1
docker run \
        -v ./src/sentinel1b/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data/:/function/src/data \
        -w /function/src \
        --env SENSOR=sentinel1b \
        --env INPUT_DIR="$1" \
        --env BOUNDS="$2" \
        --env DEM="$3" \
        --env DEM="$4" \
        --env PYTHONUNBUFFERED=0 \
        -it aoi-sentinel1b python -u main.py