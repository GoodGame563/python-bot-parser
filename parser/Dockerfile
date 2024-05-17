FROM python:3.10

RUN apt-get install -yqq --no-install-recommends \
    && pip install 'python-dateutil==2.8.2' \
    && pip install 'Telethon==1.28.5' \
    && pip install 'pymongo==4.7.1'\
    && pip install 'pyminio==0.2.1'

WORKDIR /app

ADD parser.py parser.py
ADD config.py config.py
ADD parser_functions.py parser_functions.py
ADD db.py db.py



ADD new.session new.session