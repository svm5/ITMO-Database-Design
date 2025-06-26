import time
import os
import random
import asyncio

import psycopg
from prometheus_client import start_http_server, Summary, Gauge, Counter

QUERY_TIME = Summary('fk_plus_query_duration_seconds', 'Time spent executing database query', ['query_name'])
# QUERY_TIME_GAUGE = Gauge('fk_plus_query_duration_seconds_gauge', 'Time spent executing database query (gauge)', ['query_name'])
QUERY_COUNTER = Counter('db_queries_total', 'Total number of queries')

user = os.getenv("CREATOR_NAME")
password = os.getenv("CREATOR_PASSWORD")
host = os.getenv("HOST")
port = str(os.getenv("PORT_READ"))
db = os.getenv("MY_DB")

# QUERIES = {
#     "aggregate_user_account_transactions_amount": """
#         SELECT user_accounts.id, SUM(bears_account_transactions.bears_amount)
#         FROM user_accounts 
#             INNER JOIN bears_account_transactions
#             ON user_accounts.id = bears_account_transactions.user_account_id
#         GROUP BY user_accounts.id;
#     """,
#     "sportsman_5_points": """
#         SELECT sportsmen.figure_skater_id, competitions.name, points
#         FROM competition_results
#             INNER JOIN participants
#             ON competition_results.participant_id = participants.id
#             INNER JOIN sportsmen
#             ON participants.sportsman_id = sportsmen.id
#             INNER JOIN competitions
#             ON competitions.id = participants.competition_id
#         WHERE sportsmen.figure_skater_id='5';
#     """,
#     "sportsman_photos": """SELECT single_figure_skaters.name, figure_skaters_photos.photo, figure_skaters_photos.bears_amount
#     FROM figure_skaters_photos
#         INNER JOIN sportsmen
#         ON figure_skaters_photos.sportsman_id = sportsmen.id
#         INNER JOIN single_figure_skaters
#         ON single_figure_skaters.id = sportsmen.figure_skater_id
#     WHERE single_figure_skaters.id = '1';
#     """,
#     "all_hidden_notes": """SELECT user_account_from_id, note_text
#         FROM hidden_notes
#         INNER JOIN notes
#         ON hidden_notes.note_id = notes.id
#         INNER JOIN user_accounts
#         ON notes.user_account_from_id = user_accounts.id;
#     """,
#     "sportsman_10_detailed_results": """SELECT sportsmen.figure_skater_id, perfomance_types.name, skating_skills_points, transitions_points, perfomance_points, composition_points, interpretation_points 
#     FROM sportsmen
#         INNER JOIN participants
#         ON sportsmen.id = participants.sportsman_id
#         INNER JOIN perfomance_results
#         ON perfomance_results.participant_id = participants.id
#         INNER JOIN perfomance_types
#         ON perfomance_results.perfomance_type_id = perfomance_types.id
#         LEFT JOIN components_details
#         ON perfomance_results.id = components_details.perfomance_result_id
#     WHERE sportsmen.figure_skater_id = '10';
#     """,
# }

# async def execute_query(query):
#     start_time = time.time()

#     # with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
#     #     with conn.cursor() as cursor:
#     #         # for i in range(10):
#     #         await cursor.execute(query)
#     #         _ = cursor.fetchall()
#     connection = await psycopg.AsyncConnection.connect(user=user, 
#                                                     password=password, 
#                                                     dbname=db, 
#                                                     host=host,
#                                                     port=port)
#     cursor = connection.cursor()
#     await cursor.execute(query)
#     await cursor.fetchall()    

#     await connection.close()
    
#     return time.time() - start_time

# async def monitor_queries(duration_minutes=5):
#     start_time = time.time()
#     end_time = start_time + duration_minutes * 60
#     while time.time() < end_time:
#         # query_name = random.choice(list(QUERIES.keys()))
#         for query_name in QUERIES.keys():
#             duration = await execute_query(QUERIES[query_name])
#             QUERY_TIME.labels(query_name=query_name).observe(duration)
#             # QUERY_TIME_GAUGE.labels(query_name=query_name).set(duration)
#             QUERY_COUNTER.inc()
#             await asyncio.sleep(1)
#     print("end")
# # if __name__ == "__main__":
# #     start_http_server(8000)
# #     print("Prometheus metrics server started on port 8000")
# #     for _ in range(100):
# #         asyncio.run(monitor_queries(duration_minutes=3))

# async def main(num_users):
#     start_http_server(8000)
#     tasks = [asyncio.create_task(monitor_queries(12)) for i in range(num_users)]
#     await asyncio.gather(*tasks)

# if __name__ == '__main__':
    # asyncio.run(main(num_users=1))

QUERIES = {
    "aggregate_user_account_transactions_amount": """
        SELECT user_accounts.id, SUM(bears_account_transactions.bears_amount)
        FROM user_accounts 
            INNER JOIN bears_account_transactions
            ON user_accounts.id = bears_account_transactions.user_account_id
        GROUP BY user_accounts.id;
    """,
    "aggregate_user_transfer_transactions_amount": """
        SELECT user_accounts.id, SUM(bears_transfer_transactions.bears_amount)
        FROM user_accounts 
            LEFT JOIN bears_transfer_transactions
            ON user_accounts.id = bears_transfer_transactions.user_account_from_id
        GROUP BY user_accounts.id;
    """,
    "user_subscriptions": """SELECT user_accounts.id, COUNT(user_figure_skater_subscribes.sportsman_id)
    FROM user_figure_skater_subscribes
        RIGHT JOIN user_accounts
        ON user_figure_skater_subscribes.user_account_id = user_accounts.id
    GROUP BY user_accounts.id;
    """,
    "sportsman_10_detailed_technical_results": """
    SELECT technical_elements_names.name, technical_elements_results.base_value + technical_elements_results.goe
    FROM sportsmen
        INNER JOIN participants
        ON sportsmen.id = participants.sportsman_id
        INNER JOIN perfomance_results
        ON perfomance_results.participant_id = participants.id
        INNER JOIN technical_elements_results
        ON technical_elements_results.perfomance_result_id = perfomance_results.id
        INNER JOIN technical_elements_names
        ON technical_elements_names.id = technical_elements_results.element_name_id
    WHERE sportsmen.figure_skater_id = '10';

    """,
    "sportsman_10_detailed_component_results": """SELECT sportsmen.figure_skater_id, perfomance_types.name, skating_skills_points, transitions_points, perfomance_points, composition_points, interpretation_points 
    FROM sportsmen
        INNER JOIN participants
        ON sportsmen.id = participants.sportsman_id
        INNER JOIN perfomance_results
        ON perfomance_results.participant_id = participants.id
        INNER JOIN perfomance_types
        ON perfomance_results.perfomance_type_id = perfomance_types.id
        LEFT JOIN components_details
        ON perfomance_results.id = components_details.perfomance_result_id
    WHERE sportsmen.figure_skater_id = '10';
    """,
}

def execute_query(query):
    retult = 0
    

    cnt_error = 0
    for _ in range(5):
        try:
            with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
                with conn.cursor() as cursor:
                    # for i in range(10):
                    start_time = time.time()
                    cursor.execute(query)
                    result = time.time() - start_time
                    _ = cursor.fetchall()
            break
        except:
            print("catch", cnt_error)
            cnt_error += 1
            if cnt_error >= 5:
                raise
            time.sleep(3)

    return result
    # return time.time() - start_time

def monitor_queries(duration_minutes=5):
    start_time = time.time()
    end_time = start_time + duration_minutes * 60
    while time.time() < end_time:
        for query_name in QUERIES.keys():
            duration = execute_query(QUERIES[query_name])
            QUERY_TIME.labels(query_name=query_name).observe(duration)
            QUERY_COUNTER.inc()

# if __name__ == "__main__":
#     start_http_server(8000)
#     print("Prometheus metrics server started on port 8000")
#     for _ in range(100):
#         asyncio.run(monitor_queries(duration_minutes=3))

if __name__ == '__main__':
    start_http_server(8000)
    monitor_queries(10)
