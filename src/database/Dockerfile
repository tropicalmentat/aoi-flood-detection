FROM osgeo/gdal:ubuntu-small-3.6.3

ARG USER_ID
ARG GROUP_ID

RUN apt update && \
    apt install -y --no-install-recommends \
    file python3 python3-dev 

RUN mkdir function

WORKDIR /function

COPY ./shared/ /function/shared/

COPY ./src/database /function/src/database/

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user