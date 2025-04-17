FROM python:3.8-slim

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY ./requirements.txt /usr/src/
# line below was required for psycopg2 to work for me
# I am on an M3 Mac, MacOS Sequoia 15.3.2
# RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/

CMD [ "sh", "scripts/start.sh" ]
