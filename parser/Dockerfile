FROM python:3.10

RUN apt-get install -yqq --no-install-recommends \
    && pip install 'python-dateutil==2.8.2' \
    && pip install 'Telethon==1.28.5' 

WORKDIR /app

ADD parser.py parser.py
ADD config.py config.py
ADD parser_functions.py parser_functions.py


ADD new.session new.session