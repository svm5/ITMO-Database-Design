from faker import Faker
import random

def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_subscribes(cursor):
    seed_count = 50 * int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    data = []
    cursor.execute("SELECT id FROM user_accounts")
    print("here1")
    user_account_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    cursor.execute("SELECT id FROM sportsmen")
    print("here2")
    sportsmen_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    print("here3")
    for i in range(1, seed_count + 1):
        past_date = fake.past_date()
        past_time = fake.time()
        data.append((
            i,
            user_account_ids[i-1],
            sportsmen_ids[i - 1],
            f"{past_date} {past_time}"))

    print("hello")
    query = "INSERT INTO user_figure_skater_subscribes VALUES(%s, %s, %s, %s)"
    cursor.executemany(query, data)
    print("inserted")


if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 4.0")

    SUBSCRIBES = "user_figure_skater_subscribes"

    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")

    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_subscribes(cursor)

            conn.commit()
            print("end")
