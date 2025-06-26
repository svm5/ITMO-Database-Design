from faker import Faker
import random

def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_competitions(cursor):
    seed_count = int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM cities")
    cities_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    cursor.execute("SELECT id FROM competition_types")
    competition_types_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)


    data = []
    for i in range(1, seed_count + 1):
        start = fake.past_date()
        end = fake.past_date()
        if start > end:
            start, end = end, start

        data.append((
            i,
            fake.sentence(),
            cities_ids[i - 1],
            start,
            end,
            competition_types_ids[i - 1]
        ))

    query = "INSERT INTO competitions VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)


def seed_participants(cursor):
    seed_count = 10 * int(os.getenv("SEED_COUNT"))

    cursor.execute("SELECT id FROM competitions")
    competition_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    cursor.execute("SELECT id FROM sportsmen")
    sportsmen_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    cursor.execute("SELECT id FROM categories")
    category_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            competition_ids[i - 1],
            sportsmen_ids[i - 1],
            category_ids[i - 1]
        ))

    query = "INSERT INTO participants VALUES(%s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_prediction_contests(cursor):
    seed_count = int(os.getenv("SEED_COUNT"))
  
    cursor.execute("SELECT id FROM competitions")
    competition_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    cursor.execute("SELECT id FROM categories")
    category_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            competition_ids[i - 1],
            category_ids[i - 1],
            random.choice([True, False])
        ))

    query = "INSERT INTO prediction_contests VALUES(%s, %s, %s, %s)"
    cursor.executemany(query, data)


def seed_user_prediction(cursor):
    seed_count = 30 * int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM user_accounts")
    user_account_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    cursor.execute("SELECT id FROM participants")
    participants_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            user_account_ids[i - 1],
            participants_ids[i - 1],
            fake.random_int(min=1, max=3)
        ))

    query = "INSERT INTO user_predictions VALUES(%s, %s, %s, %s)"
    cursor.executemany(query, data)

if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 5.0")

    COMPETITIONS = "competitions"
    PARTICIPANTS = "participants"
    PREDICTON_CONTESTS = "prediction_contests"
    USER_PREDICTIONS = "user_predictions"
    
    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")

    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_competitions(cursor)
            seed_participants(cursor)
            seed_prediction_contests(cursor)
            seed_user_prediction(cursor)

            conn.commit()
