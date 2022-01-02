FROM python:3.9-slim-buster
ENV PYTHONBUFFERED=1
WORKDIR /transitaz
COPY requirements.txt requirements.txt
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt