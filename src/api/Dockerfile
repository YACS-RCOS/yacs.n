FROM python:3.6-slim

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY ./requirements.txt /usr/src/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/
asdfsad
CMD [ "sh", "scripts/start.sh" ]
