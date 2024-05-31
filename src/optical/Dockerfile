FROM osgeo/gdal:ubuntu-small-3.6.3

ARG USER_ID
ARG GROUP_ID

# Orfeo toolbox dependencies
RUN apt update && \
    apt install -y --no-install-recommends \
    file python3 python3-dev python3-numpy python3-pip

RUN apt install -y --no-install-recommends \
    g++ swig cmake make

RUN mkdir function

COPY ./src/optical/requirements.txt /function/

WORKDIR /function

RUN pip3 install -U pip \
    && pip3 install --no-cache-dir -r ./requirements.txt

COPY ./src/optical/ /function/src/optical

COPY ./shared/ /function/shared/

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user