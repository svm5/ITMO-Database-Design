def is_table_empty(cursor, tablename):
    cursor.execute(f"SELECT * FROM {tablename}")
    return len(cursor.fetchall()) == 0

def seed_achivements(cursor):
    cursor.execute("""
        SELECT competitions.id AS comp_id, competitions.competition_type_id AS comp_type_id, participants.sportsman_id,  points AS p
        FROM participants 
                JOIN competitions ON participants.competition_id = competitions.id
                JOIN competition_results ON competition_results.participant_id = participants.id
        ORDER BY competitions.id, points DESC""")
    cnt = 0
    current = None
    processed_result = []
    id = 1
    for elem in cursor.fetchall():
        if elem[0] != current:
            current = elem[0]
            cnt = 0
        if cnt >= 3:
            continue
        cnt += 1
        processed_result.append((id, elem[1], elem[2], cnt))
        id += 1
    print(processed_result)

    query = "INSERT INTO achivements VALUES(%s, %s, %s, %s)"
    cursor.executemany(query, processed_result)

if __name__ == "__main__":
    import os
    import psycopg

    print("Seed migration 5.2")

    ACHIVEMENTS = "achivements"

    user = os.getenv("CREATOR_NAME")
    password = os.getenv("CREATOR_PASSWORD")
    host = os.getenv("HOST")
    port = str(os.getenv("PORT"))
    db = os.getenv("MY_DB")

    with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            seed_achivements(cursor)

            conn.commit()
