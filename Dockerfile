FROM python:3.10

WORKDIR /usr/src/app

COPY ./app .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt