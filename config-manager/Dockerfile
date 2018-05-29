FROM python:3.6.1

# Initialize
RUN mkdir -p /data/config-manager
WORKDIR /data/config-manager

# Setup

COPY requirements.txt /data/pdflist/
RUN pip3 install -r requirements.txt

#saving build time


# Prepare
COPY . /data/config-manager/

RUN mkdir -p server/static/admin