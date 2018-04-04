FROM python:3.6.1

# Initialize
RUN mkdir -p /data/ai-backend
WORKDIR /data/ai-backend

# Setup

COPY requirements.txt /data/ai-backend/
RUN pip3 install -r requirements.txt

# Prepare
COPY . /data/ai-backend/


