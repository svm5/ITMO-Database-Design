FROM python:3.8.5

RUN pip install psycopg
RUN pip install prometheus_client

COPY ./backend_imitation/backend_imitation.py .
CMD [ "python", "./backend_imitation.py" ]
