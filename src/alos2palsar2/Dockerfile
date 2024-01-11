FROM orfeotoolbox/otb:latest

RUN apt update && \
    apt install -y python3-pip

RUN mkdir function

COPY ./src/alos2palsar2/requirements.txt /function/

WORKDIR /function

RUN pip3 install -U pip \
    && pip3 install --no-cache-dir -r ./requirements.txt

COPY ./src/alos2palsar2 /function/src/alos2palsar2/

COPY ./shared/ /function/shared/
