FROM osgeo/gdal:ubuntu-small-3.6.3

# Orfeo toolbox dependencies
RUN apt update && \
    apt install -y --no-install-recommends \
    file python3 python3-dev python3-numpy

RUN apt install -y --no-install-recommends \
    g++ swig cmake make

RUN curl -O https://www.orfeo-toolbox.org/packages/OTB-8.1.2-Linux64.run