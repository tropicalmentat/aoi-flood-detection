
####################
# HELP FUNCTON
####################

while getopts ":i:f" flag; do
        case $flag in
                i) # handle image name
                arg1="$OPTARG"
                ;;
                f) # handle function to run
                ;;
        esac
done
echo ${arg1}

# TODO: assign command line arguments to environment variables
# TODO: Create help func to provide instructions on how to run the script
# TODO: Check if passed var in positional parameter exists

docker run \
        -v ./src/${arg1}/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i msgeo-${arg1} -k test_extract_sentinel1b --log-cli-level=DEBUG