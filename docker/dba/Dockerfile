FROM ubuntu:18.04
FROM python:3.6.4-alpine

RUN apk update \
  && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY . /src
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
SHELL ["/bin/bash", "-c", "./docker/dba/startup.sh"]
CMD [ "./docker/dba/wait-for-it.sh", "db"]
