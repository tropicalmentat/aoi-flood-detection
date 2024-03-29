#!/bin/bash

docker run \
        -v ./src/optical/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data:/function/src/data \
        -w /function/src \
        --env SENSOR="$1" \
        --env ALGORITHM="$2" \
        --env INPUT="$3" \
        --env OUTPUT="$4" \
        --env DB_PATH="$5" \
        -it aoi-optical python3 main.py