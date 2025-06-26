role_name="analytic"

if [[ $(psql -tXA -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "SELECT 1 FROM pg_roles WHERE rolname='$role_name';") -ne "1" ]]
then
    psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c  "CREATE ROLE $role_name WITH LOGIN;"
    psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "GRANT CONNECT ON DATABASE $MY_DB TO $role_name;"
    psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "GRANT USAGE ON SCHEMA public TO $role_name;"
    psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO $role_name;"
    psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "GRANT SELECT, USAGE ON ALL SEQUENCES IN SCHEMA public to $role_name;"
    psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO $role_name;"
    psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO $role_name;"

    for name in $(echo "$ANALYST_NAMES" | tr ',' '\n')
    do
        password="${name}_123"
        psql -h $HOST -U $POSTGRES_USER -d $MY_DB -p $PORT -c "
        CREATE USER $name WITH PASSWORD '$password';
        GRANT $role_name TO $name;"
    done
fi
