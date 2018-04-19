FROM python:2.7-slim
MAINTAINER Prasanta Kakati <prasantakakati@ekata.social>
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN mkdir -p /usr/share/man/man1
RUN mkdir -p /usr/share/man/man7
RUN apt-get install -y build-essential postgresql-client libpq-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN mkdir /code/ekatabackups
