#!/bin/bash

docker run \
        -v ./src/database:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data:/function/src/data \
        -w /function/src \
        -it aoi-db python3 main.py