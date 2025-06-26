FROM python:3.8.5

RUN pip install faker
RUN pip install psycopg

COPY ./seeding/run_seeding.py .
COPY ./seeding/scripts ./scripts

CMD [ "python", "./run_seeding.py" ]
