FROM python:3.10

RUN apt-get install -yqq --no-install-recommends \
    && pip install 'Telethon==1.25.0' 

WORKDIR /app

ADD data/db.py data/db.py
