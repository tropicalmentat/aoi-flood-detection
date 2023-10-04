
####################
# HELP FUNCTON
####################

while getopts ":s:f:i:o:" flag; do
        case $flag in
                s) # handle image name
                image="$OPTARG"
                ;;
                f) # handle function to run
                function="$OPTARG"
                ;;
                i) # handle input filepath/link
                inlink="$OPTARG"
                ;;
                o) # handle output filepath/link
                outlink="$OPTARG"
                ;;
        esac
done
echo ${image}

# TODO: assign command line arguments to environment variables
# TODO: Create help func to provide instructions on how to run the script
# TODO: Check if passed var in positional parameter exists

docker run \
        -v ./src/${image}/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i msgeo-${image} -k test_extract_sentinel1b --log-cli-level=DEBUG