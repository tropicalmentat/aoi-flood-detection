
docker build -t aoi-db --build-arg GROUP_ID=$(id -g) --build-arg USER_ID=$(id -u) -f ./src/database/Dockerfile . &&
docker build -t aoi-landsat --build-arg GROUP_ID=$(id -g) --build-arg USER_ID=$(id -u) -f ./src/optical/Dockerfile . &&
docker build -t aoi-alos2palsar2 --build-arg GROUP_ID=$(id -g) --build-arg USER_ID=$(id -u) -f ./src/alos2palsar2/Dockerfile . &&
docker build -t aoi-sentinel1b --build-arg GROUP_ID=$(id -g) --build-arg USER_ID=$(id -u) -f ./src/sentinel1b/Dockerfile . &&
docker build -t aoi-impact --build-arg GROUP_ID=$(id -g) --build-arg USER_ID=$(id -u) -f ./src/impact-assessment/Dockerfile . &&
docker build -t aoi-api --build-arg GROUP_ID=$(id -g) --build-arg USER_ID=$(id -u) -f ./src/api/Dockerfile .