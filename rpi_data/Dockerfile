FROM python:3.8.12-slim-bullseye

ADD cronjob /etc/cron.d/cronjob

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY modules ./modules/
COPY requirements.txt ./
COPY school-department-mapping.yaml ./
COPY automate-semesters.sh ./
COPY website_checker.py ./

RUN chmod +x /etc/cron.d/cronjob && \
  chmod +x /usr/src/automate-semesters.sh && \
  touch /var/log/cron.log

RUN apt update && apt install cron curl -y && \
  pip install --no-cache-dir -r requirements.txt
CMD cron && tail -f /var/log/cron.log