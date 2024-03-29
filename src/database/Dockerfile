FROM osgeo/gdal:ubuntu-small-3.6.3

RUN apt update && \
    apt install -y --no-install-recommends \
    file python3 python3-dev 

RUN mkdir function

WORKDIR /function

COPY ./shared/ /function/shared/

COPY ./src/database /function/src/database/
