
docker build -t aoi-landsat -f ./src/landsat/Dockerfile . &&
docker build -t aoi-alos2palsar2 -f ./src/landsat/Dockerfile . &&
docker build -t aoi-sentinel1b -f ./src/sentinel1b/Dockerfile . &&
docker build -t aoi-impact -f ./src/impact-assessment . &&
docker build -t aoi-api -f ./src/api/Dockerfile .