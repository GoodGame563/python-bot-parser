FROM python:3.10

RUN apt-get install -yqq --no-install-recommends \
    && pip install 'pymongo==4.7.1' 

WORKDIR /app

ADD db.py db.py

