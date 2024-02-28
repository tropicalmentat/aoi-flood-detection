#!/bin/bash

docker run \
        -v ./src/sentinel1b/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i aoi-sentinel1b -k test_flood_extract --log-cli-level=DEBUG