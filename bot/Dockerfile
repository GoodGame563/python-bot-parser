FROM python:3.10

RUN apt-get install -yqq --no-install-recommends \
    && pip install 'python-dateutil==2.8.2' \
    && pip install 'Telethon==1.28.5' \
    && pip install 'pymongo==4.7.1'\
    && pip install 'pyminio==0.2.1'\
    && pip install 'aiogram==3.6.0'\
    && pip install 'logging==0.4.9.6'

WORKDIR /app

ADD data/db.py data/db.py
