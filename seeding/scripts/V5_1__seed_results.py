from faker import Faker
import random

def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_competition_results(cursor):
    cursor.execute("SELECT participant_id, SUM(technical_elements_points + components_points) FROM perfomance_results GROUP BY participant_id")
    results = [(int(x[0]), float(x[1])) for x in cursor.fetchall()]

    data = []
    for i in range(1, len(results) + 1):
        data.append((
            i,
            results[i - 1][0],
            results[i - 1][1]
        ))

    query = "INSERT INTO competition_results VALUES(%s, %s, %s)"
    cursor.executemany(query, data)


def seed_perfomance_results(cursor):
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM participants")
    participants_ids = [int(x[0]) for x in cursor.fetchall()]

    # number of perfomance types - 4
    data = []
    for i in range(len(participants_ids)):
        first_type = fake.random_int(min=1, max=4)
        second_type = fake.random_int(min=1, max=4)
        if first_type == second_type:
            first_type = (first_type + 1) % 4
            if first_type == 0:
                first_type += 1

        data.append((
            2 * i,
            participants_ids[i - 1],
            first_type,
            fake.pyfloat(min_value=0, max_value=130),
            fake.pyfloat(min_value=0, max_value=50),
            fake.random_int(min=0, max=5)
        ))

        data.append((
            2 * i + 1,
            participants_ids[i - 1],
            second_type,
            fake.pyfloat(min_value=0, max_value=130),
            fake.pyfloat(min_value=0, max_value=50),
            fake.random_int(min=0, max=5)
        ))

    query = "INSERT INTO perfomance_results VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_components_ditails(cursor):
    seed_count = 5 * int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM perfomance_results")
    perfomance_results_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            perfomance_results_ids[i - 1],
            fake.pyfloat(min_value=0, max_value=10),
            fake.pyfloat(min_value=0, max_value=10),
            fake.pyfloat(min_value=0, max_value=10),
            fake.pyfloat(min_value=0, max_value=10),
            fake.pyfloat(min_value=0, max_value=10)
        ))

    query = "INSERT INTO components_details VALUES(%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_tech_elements_names(cursor):
    seed_count = 30
    fake = Faker("en_US")

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            fake.word()
        ))

    query = "INSERT INTO technical_elements_names VALUES(%s, %s)"
    cursor.executemany(query, data)

def seed_tech_elements_marks(cursor):
    seed_count = 10
    fake = Faker("en_US")

    data = []
    for i in range(1, seed_count + 1):
        data.append((
            i,
            fake.word()
        ))

    query = "INSERT INTO technical_elements_marks VALUES(%s, %s)"
    cursor.executemany(query, data)

    

def seed_tech_elements_results(cursor):
    seed_count = 3 * int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    cursor.execute("SELECT id FROM participants")
    participants_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    cursor.execute("SELECT id FROM technical_elements_names")
    elements_names = [int(x[0]) for x in cursor.fetchall()]

    cursor.execute("SELECT id FROM technical_elements_marks")
    elements_marks = [int(x[0]) for x in cursor.fetchall()]

    data = []
    cnt = 1
    for i in range(1, seed_count + 1):
        number = fake.random_int(min=5, max=12)
        tech_elem_names = random.choices(elements_names, k=number)
        tech_elem_marks = random.choices(elements_marks, k=number)

        for j in range(number):
            data.append((
                cnt,
                participants_ids[i - 1],
                j,
                tech_elem_names[j],
                tech_elem_marks[j],
                fake.pyfloat(min_value=1, max_value=20),
                fake.random_int(min=-5, max=5)
            ))
            cnt += 1

    query = "INSERT INTO technical_elements_results VALUES(%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)    


if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 5.1")

    COMPETITION_RESULTS = "competition_results"
    PERFOMANCE_RESULTS = "perfomance_results"
    COMPONENTS_DETAILS = "components_details"
    TECH_ELEMS_NAMES = "technical_elements_names"
    TECH_ELEMS_MARKS = "technical_elements_marks"
    TECH_ELEMS_RESULTS = "technical_elements_results"
    
    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")

    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_tech_elements_names(cursor)
            seed_tech_elements_marks(cursor)
            seed_perfomance_results(cursor)
            seed_components_ditails(cursor)
            seed_tech_elements_results(cursor)
            seed_competition_results(cursor)

            conn.commit()
