FROM ubuntu:16.04
FROM python:3.6.5

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \ 
    apt-get install -y curl wget && \
    apt-get install -y default-jre

WORKDIR /app
COPY . /app
RUN pip install -r /app/requirements.txt
RUN pip install /app/lib/datarobot_mlops-6.2.0-py2.py3-none-any.whl 

ARG ENDPOINT='YOUR DR ENDPOINT'
ARG TOKEN='YOUR DR API TOKEN'
ARG USERNAME='felix.huthmacher@datarobot.com'
ARG PROJECT_ID='YOUR DEFAULT PROJECT_ID'
ARG MODEL_ID='YOUR DEFAULT MODEL_ID'
ARG CHANNEL_CONFIG='YOUR MLOPS CHANNEL CONFIG'
ARG DEPLOYMENT_ID='YOUR MLOPS DEPLOYMENT_ID'
ARG MLOPS_MODELID='YOUR MLOPS MODEL ID'

ENV DATAROBOT_ENDPOINT=$ENDPOINT
ENV DATAROBOT_API_TOKEN=$TOKEN
ENV USERNAME=$USERNAME
ENV PROJECT_ID=$PROJECT_ID
ENV MODEL_ID=$MODEL_ID
ENV CHANNEL_CONFIG=$CHANNEL_CONFIG
ENV DEPLOYMENT_ID=$DEPLOYMENT_ID
ENV MLOPS_MODELID=$MLOPS_MODELID
RUN mkdir tmp
CMD python /app/model.py && python /app/drmodel.py && python /app/server.py
