#!/bin/bash

docker run \
        -v ./src/optical/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data:/function/src/data \
        -w /function/src \
        --env SENSOR="$1" \
        --env INPUT="$2" \
        --env OUTPUT="$3" \
        -it aoi-optical python3 main.py