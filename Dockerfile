FROM alpine:latest
LABEL maintainer Prasanta Kakati <prasantakakati@ekata.social>
RUN apk update
RUN apk add build-base postgresql-client postgresql-dev libpq python2 python2-dev py-pip nodejs nodejs-npm
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
RUN npm install 
RUN mkdir /code/ekatabackups
