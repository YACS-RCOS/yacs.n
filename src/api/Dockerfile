FROM python:3.8-slim

ENV PYTHONPATH=/usr/src

RUN mkdir -p /usr/src

RUN apt-get update && apt-get install -y gcc

WORKDIR /usr/src
COPY ./requirements.txt /usr/src/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/

CMD [ "sh", "scripts/start.sh" ]
