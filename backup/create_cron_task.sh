#! /bin/bash
# echo "hello, cron! -> 1 <-"
# ls
# touch "abc.txt"
# now=$(date +"%Y_%m_%d__%H_%M_%S")
# echo "$now" >> "abc.txt"
# echo "BACKUP_RETENTION_COUNT $BACKUP_RETENTION_COUNT BACKUP_INTERVAL_CRON $BACKUP_INTERVAL_CRON CREATOR_NAME $CREATOR_NAME CREATOR_PASSWORD $CREATOR_PASSWORD MY_DB $MY_DB HOST $HOST PORT $PORT" >> "abc.txt"

# echo "1 * * * * /bin/bash ./create_backup.sh >> /var/log/cron.log 2>&1" > my_crontab

# crontab my_crontab

crontab -l | { cat; echo "*/$BACKUP_INTERVAL_CRON * * * * /create_backup.sh $BACKUP_RETENTION_COUNT $CREATOR_NAME $CREATOR_PASSWORD $MY_DB $HOST $PORT >> /var/log/cron.log 2>&1"; } | crontab -
