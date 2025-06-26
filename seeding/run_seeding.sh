#! /bin/bash


if [[ "$APP_ENV" == "dev" ]]
then
    for elem in $(ls "./scripts")
    do
        python "./scripts/$elem"
    done
fi
