def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_categories(cursor):
    categories = [
        (1, 'Man'),
        (2, 'Woman'),
        (3, 'Pairs'),
        (4, 'Ice dancing'),
        (5, 'Junior man'),
        (6, 'Junior woman'),
        (7, 'Junior pairs'),
        (8, 'Junior ice dancing')
    ]

    query = "INSERT INTO categories VALUES(%s, %s)"
    cursor.executemany(query, categories)


def seed_competition_types(cursor):
    competition_types = [
        (1, 'Russian Championship'),
        (2, 'International Grand Prix'),
        (3, 'Russian Grand Prix'),
        (4, 'Grand Prix Final'),
        (5, 'Russian Grand Prix Final'),
        (6, 'European Championship'),
        (7, 'World Cup'),
        (8, 'Olympic Games'),
        (9, 'Four Continents Championships')
    ]

    query = "INSERT INTO competition_types VALUES(%s, %s)"
    cursor.executemany(query, competition_types)

def seed_perfomance_types(cursor):
    perfomance_types = [
        (1, 'Short program'),
        (2, 'Free program'),
        (3, 'Rhythm dance'),
        (4, 'Free dance'),
        (5, 'Show program')
    ]
    
    query = "INSERT INTO perfomance_types VALUES(%s, %s)"
    cursor.executemany(query, perfomance_types)

def seed_cities(cursor):
    from faker import Faker

    fake = Faker("en_US")
    cities = []
    for i in range(1, 51):
        cities.append((i, fake.country(), fake.city()))

    query = "INSERT INTO cities VALUES(%s, %s, %s)"
    cursor.executemany(query, cities)

if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 1")

    CATEGORIES = "categories"
    COMPETITION_TYPES = "competition_types"
    PERFOMANCE_TYPES = "perfomance_types"
    CITIES = "cities"


    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")

    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_categories(cursor)
            seed_competition_types(cursor)
            seed_perfomance_types(cursor)
            seed_cities(cursor)

            conn.commit()
