FROM python:3.6.4 
COPY stock_exchange/requirements.txt /src/
WORKDIR /src/
RUN pip install -r requirements.txt
COPY . /src/
CMD [ "./docker/app/startup.sh" ]