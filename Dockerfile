FROM python:3.8-alpine
MAINTAINER Ahmed Emad.
ENV PYTHONUNBUFFERED 1
RUN mkdir /unotesapi
WORKDIR /unotesapi
COPY . /unotesapi
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN apk add --update --no-cache postgresql-client postgresql jpeg-dev zlib-dev libjpeg
RUN pip3 install -r /unotesapi/requirements.txt
RUN apk del .tmp-build-deps
RUN adduser -D unotesapi
USER unotesapi