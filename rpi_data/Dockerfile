FROM debian:stretch

ADD cronjob /etc/cron.d/cronjob

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY modules ./modules/
COPY requirements.txt ./
ADD automate-semesters.sh ./
ADD website_checker.py ./

RUN chmod +x /etc/cron.d/cronjob
RUN chmod +x /usr/src/automate-semesters.sh
RUN touch /var/log/cron.log

RUN apt update && apt install cron python3-pip python3 -y
RUN pip3 install --no-cache-dir -r requirements.txt
CMD cron && tail -f /var/log/cron.log