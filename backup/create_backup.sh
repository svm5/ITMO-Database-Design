#! /bin/bash

BACKUP_RETENTION_COUNT="$1"
CREATOR_NAME="$2"
CREATOR_PASSWORD="$3"
MY_DB="$4"
HOST="$5"
PORT="$6"

dirname="fk_db_backups"
if [[ ! -d "/$dirname" ]]
then
    mkdir "/$dirname"
fi

now=$(date +"%Y_%m_%d__%H_%M_%S")
# touch "/$dirname/file_$now.txt"
# echo "BACKUP_RETENTION_COUNT $BACKUP_RETENTION_COUNT BACKUP_INTERVAL_CRON $BACKUP_INTERVAL_CRON" >> "/$dirname/file_$now.txt"

pg_dump --dbname="postgresql://$CREATOR_NAME:$CREATOR_PASSWORD@$HOST:$PORT/$MY_DB" > /$dirname/fk_$now.dump

files_cnt=$(ls /$dirname | wc -l)

if [[ "$files_cnt" > "$BACKUP_RETENTION_COUNT" ]]
then 
    cnt_to_remove=$(("$files_cnt" - "$BACKUP_RETENTION_COUNT")) 
    for name in $(ls /$dirname | head -n "$cnt_to_remove")
    do
        # echo "rm /$dirname/$name" >> "/$dirname/file_$now.txt"
        rm "/$dirname/$name"
    done
fi
