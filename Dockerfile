FROM python:3.8-slim

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT wsgi

