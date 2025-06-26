FROM ubuntu:latest

# Install cron and any other dependencies
RUN apt-get update && apt-get install -y cron && apt-get install -y postgresql-client

ARG BACKUP_RETENTION_COUNT
ARG BACKUP_INTERVAL_CRON
ARG CREATOR_NAME
ARG CREATOR_PASSWORD
ARG MY_DB
ARG HOST
ARG PORT

ENV BACKUP_RETENTION_COUNT $BACKUP_RETENTION_COUNT
ENV BACKUP_INTERVAL_CRON $BACKUP_INTERVAL_CRON
ENV CREATOR_NAME $CREATOR_NAME
ENV CREATOR_PASSWORD $CREATOR_PASSWORD
ENV MY_DB $MY_DB
ENV HOST $HOST
ENV PORT $PORT

# ENV BACKUP_RETENTION_COUNT=2
# ENV BACKUP_INTERVAL_CRON=1

COPY ./backup/create_backup.sh .
COPY ./backup/create_cron_task.sh .


RUN chmod 700 ./create_cron_task.sh
RUN chmod 700 ./create_backup.sh
RUN ./create_cron_task.sh

# Copy crontab file to the cron.d directory
# COPY crontab /etc/cron.d/my-cron-job

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply cron job
# RUN crontab /etc/cron.d/my-cron-job

RUN touch /var/log/cron.log && chmod 666 /var/log/cron.log

# Run the command on container startup
CMD ["cron", "-f"]
# ENTRYPOINT [ "./create_cron_task.sh" ]
