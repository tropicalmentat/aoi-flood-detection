#!/bin/bash

docker run \
        -v ./src/impact-assessment/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data:/function/src/data \
        -w /function/src \
        --env SENSOR="$1" \
        --env BOUNDS="$2" \
        --env DB_PATH="$3" \
        --env OUTPUT="$4" \
        --env EVENT="$5" \
        --env LOCATION="$6" \
	--env POVERTY_INCIDENCE="$7" \
        -it aoi-impact python3 main.py
