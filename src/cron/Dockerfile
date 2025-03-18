# FROM selenium/standalone-firefox:latest
FROM python:3.9-slim


RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl

RUN apt-get update && apt-get -y install cron vim
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN touch /var/log/cron.log

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY ./requirements.txt /usr/src/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/

CMD ["cron", "-f"]