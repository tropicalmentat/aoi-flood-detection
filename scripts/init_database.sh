#!/bin/bash

docker run \
        -v ./data:/function/data \
        -w /function \
        -it aoi-db python3 database.py