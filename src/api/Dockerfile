FROM osgeo/gdal:ubuntu-small-3.6.3

RUN apt update && \
    apt install -y python3-pip

RUN mkdir function

COPY ./src/api/requirements.txt /function/

WORKDIR /function

RUN pip3 install -U pip \
    && pip3 install --no-cache-dir -r ./requirements.txt

COPY ./src/api /function/src/api

COPY ./shared/ /function/shared

EXPOSE 8000
