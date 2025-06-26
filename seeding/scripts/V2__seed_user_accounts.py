from faker import Faker
import random

def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_user_accounts(cursor):
    seed_count = 10 * int(os.getenv("SEED_COUNT"))

    fake = Faker("en_US")

    cursor.execute("SELECT id FROM cities")
    cities_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k = seed_count)
    user_accounts = []
    for i in range(1, seed_count + 1):
        past_date = fake.past_date()
        past_time = fake.time()
        user_accounts.append((
            i,
            fake.name(),
            fake.sentence(),
            fake.email(),
            0,
            cities_ids[i - 1],
            fake.file_path(),
            f"{past_date} {past_time}"))

    query = "INSERT INTO user_accounts VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, user_accounts)

def seed_user_secrets(cursor):
    seed_count = 10 * int(os.getenv("SEED_COUNT"))

    fake = Faker("en_US")

    user_secrets = []
    for i in range(1, seed_count + 1):
        user_secrets.append((i, fake.md5(raw_output=False)))

    query = "INSERT INTO user_secrets VALUES(%s, %s)"
    cursor.executemany(query, user_secrets)

if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 2")

    USER_ACCOUNTS = "user_accounts"
    USER_SECRETS = "user_secrets"

    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")
    
    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_user_accounts(cursor)
            seed_user_secrets(cursor)
            conn.commit()
