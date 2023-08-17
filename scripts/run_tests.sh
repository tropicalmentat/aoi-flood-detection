echo "Running tests"

docker system prune -f

docker run \
        -v ./src/alos2palsar2/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i msgeo-alos2palsar2 -k test_extract --log-cli-level=DEBUG