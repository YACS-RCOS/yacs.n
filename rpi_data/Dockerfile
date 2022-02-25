FROM debian:stretch


ADD cronjob /etc/cron.d/cronjob

RUN chmod +x /etc/cron.d/cronjob

RUN touch /var/log/cron.log

RUN apt update
RUN apt install cron -y

CMD cron && tail -f /var/log/cron.log