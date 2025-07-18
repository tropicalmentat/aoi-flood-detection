echo "Running tests"

docker system prune -f

docker run \
        -v ./src/sentinel1b/:/function/src \
        -v ./shared/:/function/shared \
        -v ./tests/data:/function/src/tests/data \
        -w /function/src \
        --entrypoint pytest \
        -i aoi-sentinel1b -k test_extract --log-cli-level=DEBUG
# docker run \
        # -v ./src/alos2palsar2/:/function/src \
        # -v ./shared/:/function/shared \
        # -v ./tests/data:/function/src/tests/data \
        # -w /function/src \
        # --entrypoint pytest \
        # -i aoi-alos2palsar2 -k test_extract_flood --log-cli-level=DEBUG

# docker run \
#         -v ./src/landsat/:/function/src \
#         -v ./shared/:/function/shared \
#         -v ./tests/data:/function/src/tests/data \
#         -w /function/src \
#         --entrypoint pytest \
#         -i msgeo-landsat8 -k test_extract_flood --log-cli-level=DEBUG
# docker run \
        # -v ./src/impact-assessment/:/function/src \
        # -v ./shared/:/function/shared \
        # -v ./data:/function/src/tests/data \
        # -w /function/src \
        # --entrypoint pytest \
        # -i aoi-impact -k test_execute --log-cli-level=DEBUG