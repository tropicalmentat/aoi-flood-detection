#!/bin/bash

docker run \
        -v ./src/alos2palsar2/:/function/src \
        -v ./shared/:/function/src/shared \
        -v ./data:/function/src/data \
        -w /function/src \
        -it aoi-alos2palsar2 python3 main.py