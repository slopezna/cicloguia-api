FROM python:3.9-buster

ENV PYTHONPATH="/home/services"
WORKDIR /home/services

COPY cicloguia/requirements.txt /tmp

RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

COPY cicloguia/ ./cicloguia
RUN pip install -e cicloguia