echo "Running tests"

docker system prune -f

# docker run \
        # -v ./src/sentinel1b/:/function/src \
        # -v ./shared/:/function/shared \
        # -v ./tests/data:/function/src/tests/data \
        # -w /function/src \
        # --entrypoint pytest \
        # -i msgeo-sentinel1b -k test_preprocess --log-cli-level=DEBUG
docker run \
        -v ./src/alos2palsar2/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i msgeo-alos2palsar2 -k test_extract_flood --log-cli-level=DEBUG