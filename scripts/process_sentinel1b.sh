#!/bin/bash

# docker run \
        # -v ./src/sentinel1b/:/function/src \
        # -v ./shared/:/function/src/shared \
        # -v ./data/:/function/src/data \
        # -w /function/src \
        # --env SENSOR=sentinel1b \
        # --env INPUT_DIR="$1" \
        # --env BOUNDS="$2" \
        # --env DEM="$3" \
        # --env OUTPUT="$4" \
        # --env DB_PATH="$5" \
        # -it aoi-sentinel1b python main.py

docker run \
        -v ./src/impact-assessment/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data/:/function/src/data \
        -w /function/src \
        --env BOUNDS="./data/National_PopAHS_PSA_2020.shp" \
        --env DB_PATH="./data/source.db" \
        -it aoi-impact-assessment python main.py