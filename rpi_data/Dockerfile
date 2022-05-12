FROM python:3.8.12-slim-bullseye

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY modules ./modules/
COPY requirements.txt ./
COPY school-department-mapping.yaml ./
COPY automate-semesters.sh ./
COPY website_checker.py ./

RUN apt update && apt install cron curl -y && \
  pip install --no-cache-dir -r requirements.txt && \
  chmod 0644 automate-semesters.sh && \
  crontab -l | { cat; echo "0 1 * * * bash /usr/src/automate-semesters.sh"; } | crontab -

CMD cron