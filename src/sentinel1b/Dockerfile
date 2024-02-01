FROM orfeotoolbox/otb:latest
FROM osgeo/gdal:ubuntu-small-3.6.3

RUN apt update && \
    apt install -y python3-pip

RUN mkdir function

COPY ./src/sentinel1b/requirements.txt /function/

WORKDIR /function

RUN pip3 install -U pip \
    && pip3 install --no-cache-dir -r ./requirements.txt

COPY ./src/sentinel1b /function/src/sentinel1b/

COPY ./shared/ /function/shared/
