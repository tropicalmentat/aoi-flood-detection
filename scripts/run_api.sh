docker system prune -f

docker run \
    -p "8000:8000" \
    -v ./src/api:/function/src \
    -v ./tests/data:/function/src/tests/data \
    -w /function/src \
    --entrypoint "gunicorn" \
    -i msgeo-aoi-api:latest app:app -b 0.0.0.0:8000