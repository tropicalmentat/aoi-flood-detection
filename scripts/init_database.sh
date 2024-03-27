#!/bin/bash

docker run \
        -v ./data:/function/data \
        -it aoi-db python3 database.py