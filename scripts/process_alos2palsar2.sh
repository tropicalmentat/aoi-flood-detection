#!/bin/bash

docker run \
        -v ./src/alos2palsar2/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data:/function/src/data \
        -w /function/src \
        --env INPUT_DIR="$1" \
        --env OUTPUT="$2" \
        --env DB_PATH="$3" \
        --env EVENT="$4" \
        --env LOCATION="$5" \
        -it aoi-alos2palsar2 python3 main.py