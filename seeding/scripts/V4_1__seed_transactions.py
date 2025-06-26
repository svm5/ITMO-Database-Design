from faker import Faker
import random

def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_account_transactions(cursor):
    print("account")
    seed_count = 30 * int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    data = []
    cursor.execute("SELECT id FROM user_accounts")
    user_account_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)
    comments = random.choices(["login", "present", "from contest"], k=seed_count)
    for i in range(1, seed_count):
        past_date = fake.past_date()
        past_time = fake.time()

        data.append((
            i,
            user_account_ids[i - 1],
            fake.random_int(min=10, max=30),
            "replenish",
            comments[i - 1],
            f"{past_date} {past_time}"
        ))

    query = "INSERT INTO bears_account_transactions VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)

def seed_transfer_transactions(cursor):
    print("transfer")
    seed_count = 30 * int(os.getenv("SEED_COUNT"))
    fake = Faker("en_US")

    data = []
    
    cursor.execute("SELECT id FROM user_accounts")
    user_account_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)
    
    cursor.execute("SELECT id FROM sportsmen")
    sportsmen_ids = random.choices([int(x[0]) for x in cursor.fetchall()], k=seed_count)

    comments = random.choices(["photo", "note", "nickname", "other"], k=seed_count)

    for i in range(1, seed_count):
        past_date = fake.past_date()
        past_time = fake.time()
        data.append((
            i,
            user_account_ids[i - 1],
            sportsmen_ids[i - 1],
            fake.random_int(min=1, max=9),
            comments[i - 1],
            f"{past_date} {past_time}"
        ))

    query = "INSERT INTO bears_transfer_transactions VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, data)

def update_info(cursor):
    cursor.execute("SELECT user_account_id, SUM(bears_amount) FROM bears_account_transactions GROUP BY user_account_id")
    result_1 = cursor.fetchall()
    st = set()
    d_1 = dict()
    for elem in result_1:
        d_1[elem[0]] = int(elem[1])
        st.add(elem[0])
    cursor.execute("SELECT user_account_from_id, SUM(bears_amount) FROM bears_transfer_transactions GROUP BY user_account_from_id")
    result_2 = cursor.fetchall()
    d_2 = dict()
    for elem in result_2:
        d_2[elem[0]] = int(elem[1])
        st.add(elem[0])

    for id in st:
        a = 0
        b = 0
        if id in d_1:
            a = d_1[id]
        if id in d_2:
            b = d_2
        cursor.execute(f"UPDATE user_accounts SET bears_amount='{abs(a - b)}' WHERE id='{id}'")

    cursor.execute("""SELECT sportsmen.figure_skater_id, sportsmen.figure_skater_type, SUM(bears_amount)
                       FROM bears_transfer_transactions 
                       INNER JOIN sportsmen 
                       ON bears_transfer_transactions.sportsman_id = sportsmen.id 
                       GROUP BY sportsmen.figure_skater_id, sportsmen.figure_skater_type""")
    for id, type, amount in cursor.fetchall():
        if type == "single":
            table_name = "single_figure_skaters"
        else:
            table_name = "figure_skater_pairs"
        cursor.execute(f"UPDATE {table_name} SET bears_amount='{amount}' WHERE id='{id}'")

if __name__ == "__main__":
    print("script 4_1")

    import os
    print(os.getenv("SEED_COUNT"))

    import psycopg

    ACCOUNT_TRANSACTIONS = "bears_account_transactions"
    TRANSFER_TRANSACTIONS = "bears_transfer_transactions"

    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")
    
    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_account_transactions(cursor)
            seed_transfer_transactions(cursor)
            conn.commit()
            # update_info(cursor)
            # conn.commit()
