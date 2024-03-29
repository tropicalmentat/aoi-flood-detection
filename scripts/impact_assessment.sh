#!/bin/bash

docker run \
        -v ./src/impact-assessment/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data/:/function/src/data \
        -w /function/src \
        --env SENSOR="alos2palsar2" \
        --env BOUNDS="./data/National_PopAHS_PSA_2020.shp" \
        --env DB_PATH="./data/source.db" \
        --env OUTPUT="./data/OUTPUT" \
        -it aoi-impact python main.py
        # --env SENSOR="$1" \
        # --env BOUNDS="$2" \
        # --env DB_PATH="$3" \
        # --env OUTPUT="$4" \