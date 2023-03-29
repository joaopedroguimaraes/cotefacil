# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster

WORKDIR /pedidoeletronico

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY pedidoeletronico/ .

ENTRYPOINT [ "python", "./main.py" ]