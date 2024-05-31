
docker build -t aoi-landsat -f ./src/optical/Dockerfile . &&
docker build -t aoi-alos2palsar2 -f ./src/alos2palsar2/Dockerfile . &&
docker build -t aoi-sentinel1b -f ./src/sentinel1b/Dockerfile . &&
docker build -t aoi-impact -f ./src/impact-assessment/Dockerfile . &&
docker build -t aoi-api -f ./src/api/Dockerfile .