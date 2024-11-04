FROM python:3.9

RUN apt-get install -yqq --no-install-recommends 

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD . .

COPY telegram_bot telegram_bot
WORKDIR /app/telegram_bot

CMD [ "python","main.py" ]