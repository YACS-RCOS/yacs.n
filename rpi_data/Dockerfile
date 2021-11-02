FROM ubuntu:latest

# Add cron_update file in the cron directory
ADD cron_update /etc/cron.daily/cron_update

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron_update

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log