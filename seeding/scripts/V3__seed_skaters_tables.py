import random
from faker import Faker
 
def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_single_figure_skaters(cursor):
    seed_count = int(os.getenv("SEED_COUNT"))

    fake = Faker("en_US")

    category_ids = random.choices([1, 2, 5, 6], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            fake.name(),
            0,
            fake.file_path(),
            fake.country(),
            fake.date_of_birth(),
            fake.user_name(),
            category_ids[i - 1],
            random.choice([True, False])))

    query = "INSERT INTO single_figure_skaters VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_figure_skater_pairs(cursor):
    seed_count = int(os.getenv("SEED_COUNT")) // 2
    fake = Faker("en_US")

    data = []
    category_ids = random.choices([3, 4, 7, 8], k=seed_count)

    for i in range(1, seed_count + 1):
        data.append((
            i,
            fake.first_name_female(),
            fake.first_name_male(),
            0,
            fake.file_path(),
            fake.country(),
            fake.date_of_birth(),
            fake.date_of_birth(),
            fake.user_name(),
            category_ids[i - 1],
            random.choice([True, False])))

    query = "INSERT INTO figure_skater_pairs VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_sportsmen(cursor):
    seed_count = int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    data = []
    cursor.execute("SELECT id FROM single_figure_skaters")
    single_ids = cursor.fetchall()
    for i in range(len(single_ids)):
        data.append((i, int(single_ids[i][0]), "single"))

    cursor.execute("SELECT id FROM figure_skater_pairs")
    pairs_ids = cursor.fetchall()
    for i in range(len(pairs_ids)):
        data.append((len(single_ids) + i, int(pairs_ids[i][0]), "pair"))

    query = "INSERT INTO sportsmen VALUES(%s, %s, %s)"
    cursor.executemany(query, data)

if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 3")

    SINGLE_FIGURE_SKATERS = "single_figure_skaters"
    FIGURE_SKATER_PAIRS = "figure_skater_pairs"
    SPORTSMEN = "sportsmen"

    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")

    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_single_figure_skaters(cursor)
            seed_figure_skater_pairs(cursor)
            seed_sportsmen(cursor)

            conn.commit()
