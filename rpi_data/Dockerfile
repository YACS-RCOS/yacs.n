FROM ubuntu:20.04.1 LTS

MAINTAINER 

ADD cronjob /etc/cron.d/cronjob

RUN chmod +x /etc/cron.d/cronjob

COPY ./chronjob 

COPY ./automate-semesters.sh

RUN chmod +x /automate-semesters.sh

CMD cron && tail -f /var/log/cron.log 




