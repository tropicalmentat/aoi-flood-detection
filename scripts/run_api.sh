docker system prune -f

docker run \
    -p "8000:8000" \
    -v ./src/api:/function/src \
    -v ./data:/function/src/data \
    -w /function/src \
    --entrypoint "gunicorn" \
    -i aoi-api:latest --log-level DEBUG app:app -b 0.0.0.0:8000