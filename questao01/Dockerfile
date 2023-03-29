# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster

WORKDIR /compraagora

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY compraagora/ .

ENTRYPOINT [ "python", "./main.py" ]