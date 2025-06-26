from faker import Faker
import random

def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0


def seed_nicknames(cursor):
    seed_count = int(os.getenv("SEED_COUNT")) // 2
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM sportsmen")
    sportsmen_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            fake.user_name(),
            sportsmen_ids[i - 1],
            fake.random_int(min=1, max=100)
        ))

    query = "INSERT INTO figure_skaters_nicknames VALUES(%s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_photos(cursor):
    seed_count = int(os.getenv("SEED_COUNT")) // 2
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM sportsmen")
    sportsmen_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            fake.file_path(),
            sportsmen_ids[i - 1],
            fake.random_int(min=1, max=100)
        ))

    query = "INSERT INTO figure_skaters_photos VALUES(%s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_notes(cursor):
    seed_count = 2 * int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM user_accounts")
    user_account_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)
    
    cursor.execute("SELECT id FROM sportsmen")
    sportsmen_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        past_date = fake.past_date()
        past_time = fake.time()

        data.append((
            i,
            user_account_ids[i - 1],
            sportsmen_ids[i - 1],
            fake.text(),
            f"{past_date} {past_time}",
            fake.random_int(min=1, max=100)
        ))

    query = "INSERT INTO notes VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_hidden_notes(cursor):
    seed_count = int(os.getenv("SEED_COUNT")) // 2
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM user_accounts")
    user_account_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)
    
    cursor.execute("SELECT id FROM notes")
    notes_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            user_account_ids[i - 1],
            notes_ids[i - 1]
        ))

    query = "INSERT INTO hidden_notes VALUES(%s, %s, %s)"
    cursor.executemany(query, data)


if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 4.2")

    NICKNAMES = "figure_skaters_nicknames"
    PHOTOS = "figure_skaters_photos"
    NOTES = "notes"
    HIDDEN_NOTES = "hidden_notes"

    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")

    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_nicknames(cursor)
            seed_photos(cursor)
            seed_notes(cursor)
            seed_hidden_notes(cursor)

            conn.commit()
