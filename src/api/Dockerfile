FROM python:3.8-slim

# this should be the path to the volume defined in docker-compose
WORKDIR /usr/src

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "sh", "scripts/start.sh" ]
