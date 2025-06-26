#! /bin/bash

if [[ -z $MIGRATION_VERSION ]]
then
flyway -user=$USER -password=$PASSWORD -url=jdbc:postgresql://$HOST:$PORT/$DB migrate
else
flyway -user=$USER -password=$PASSWORD -url=jdbc:postgresql://$HOST:$PORT/$DB -target="$MIGRATION_VERSION"? migrate
fi
