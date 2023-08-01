FROM osgeo/gdal:ubuntu-small-3.6.3

# Orfeo toolbox dependencies
RUN apt update && \
    apt install -y --no-install-recommends \
    file python3 python3-dev python3-numpy python3-pip

RUN apt install -y --no-install-recommends \
    g++ swig cmake make

RUN mkdir function

RUN curl -O https://www.orfeo-toolbox.org/packages/OTB-8.1.2-Linux64.run

COPY ./requirements.txt /function/

COPY ./tests /function/tests/

WORKDIR /function

RUN pip3 install -U pip \
    && pip3 wheel --no-cache-dir -r ./requirements.txt