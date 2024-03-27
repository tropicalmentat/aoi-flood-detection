FROM ubuntu:jammy

RUN mkdir function

WORKDIR /function

COPY ./shared/database.py /function

RUN apt update && \
    apt install -y --no-install-recommends \
    file python3 python3-dev 