
echo ${1}

# TODO: assign command line arguments to environment variables
# TODO: Create help func to provide instructions on how to run the script

docker run \
        -v ./src/${1}/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i msgeo-${1} -k test_extract_sentinel1b --log-cli-level=DEBUG