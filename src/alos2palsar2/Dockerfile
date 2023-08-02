FROM orfeotoolbox/otb:latest

RUN apt update && \
    apt install -y python3-pip

RUN mkdir function

RUN curl -O https://www.orfeo-toolbox.org/packages/OTB-8.1.2-Linux64.run

COPY requirements.txt /function/

COPY ./tests /function/tests/

WORKDIR /function

RUN pip3 install -U pip \
    && pip3 install --no-cache-dir -r ./requirements.txt

# COPY ./src/landsat/landsat_extract.py /function/src/landsat
COPY ./shared/utils.py /function/shared/

COPY ./shared/preprocess/ /function/shared/preprocess/