FROM python:3.12

RUN apt-get install -yqq --no-install-recommends 

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD data/base_connection_db.py data/base_connection_db.py
ADD data/key_words_db.py data/key_words_db.py
ADD data/minio_function.py data/minio_function.py
ADD data/settings_db.py data/settings_db.py
ADD data/telegram_channel_db.py data/telegram_channel_db.py
ADD __init__.py __init__.py

ADD logs/__init__.py logs/__init__.py 
ADD logs/loging.py logs/loging.py

ADD parser/__init__.py parser/__init__.py
ADD parser/parser_functions.py parser/parser_functions.py
ADD parser/parser.py parser/parser.py

COPY telegram_bot telegram_bot
WORKDIR /app/telegram_bot

CMD [ "python","main.py" ]