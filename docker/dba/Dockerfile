
FROM python:3.6.4-alpine
RUN apk update \
  && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq
COPY stock_exchange/requirements.txt /src/
WORKDIR /src/
RUN pip install -r requirements.txt
COPY . /src/
CMD [ "./docker/dba/wait-for-it.sh", "db", "./docker/dba/startup.sh" ]