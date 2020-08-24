FROM alpine:latest
LABEL maintainer Prasanta Kakati <prasantakakati@ekata.social>
RUN apk update
RUN apk add build-base linux-headers postgresql-client postgresql-dev libpq python2 python2-dev py-pip nodejs nodejs-npm zlib-dev jpeg-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code
RUN npm install 
RUN mkdir /code/ekatabackups
