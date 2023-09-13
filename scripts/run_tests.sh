echo "Running tests"

docker system prune -f

docker run \
        -v ./src/sentinel1b/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i msgeo-sentinel1b -k test_extract_sentinel1b --log-cli-level=DEBUG