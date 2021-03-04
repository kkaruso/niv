FROM ubuntu:latest

COPY . /app

CMD python /app/main.py
