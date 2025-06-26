def get_migration_number(filename: str):
    filename = filename[1:]
    number_part, _ = filename.split("__")
    return list(map(int, number_part.split('_')))

def compare_versions(last_number, current_number):
    if len(last_number) < len(current_number):
        while len(last_number) != len(current_number):
            last_number.append(0)
    if len(last_number) > len(current_number):
        while len(last_number) != len(current_number):
            current_number.append(0)
    
    for i in range(len(last_number)):
        if last_number[i] > current_number[i]:
            return True
        if last_number[i] < current_number[i]:
            return False
    return True

if __name__ == "__main__":
    import os

    app_env = user = os.getenv("APP_ENV")
    if app_env == "dev":
        migration_number = None
        if os.getenv("MIGRATION_VERSION") is not None:
            migration_number = list(map(int, os.getenv("MIGRATION_VERSION").split('.')))
        
        import psycopg

        SEEDING_INFO_TABLE = "seeding_info_table"
        user = os.getenv("CREATOR_NAME")
        password = os.getenv("CREATOR_PASSWORD")
        host = os.getenv("HOST")
        port = str(os.getenv("PORT"))
        db = os.getenv("MY_DB")

        seeding_table_data = []
        seeding_table_filenames = []
        with psycopg.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}") as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'""")
                table_names = [elem[0] for elem in cursor.fetchall()]
                if SEEDING_INFO_TABLE in table_names:
                    cursor.execute(f"SELECT * FROM {SEEDING_INFO_TABLE}")
                    seeding_table_data = cursor.fetchall()
                else:
                    cursor.execute(f"""
                                    CREATE TABLE {SEEDING_INFO_TABLE} (
                                        id SERIAL PRIMARY KEY,
                                        version_name VARCHAR(300) NOT NULL
                                    );
                                """)
                print("Seeding table data", seeding_table_data)
                seeding_table_filenames = [x[1] for x in seeding_table_data]

                import subprocess
                result = subprocess.run(["ls", "./scripts"], capture_output=True, text=True)
                filenames = result.stdout.split("\n")
                print("Filenames", filenames)
                for filename in filenames:
                    if not filename.count("__"):
                        continue
                    if filename in seeding_table_filenames:
                        continue
                    if migration_number is not None:
                        if not compare_versions(migration_number, get_migration_number(filename)):
                            continue
            
                    print(filename, get_migration_number(filename))
                    subprocess.run(["python", f"./scripts/{filename}"])
                    cursor.execute(f"INSERT INTO {SEEDING_INFO_TABLE}(version_name) VALUES('{filename}')")

        # filenames = os.listdir("scripts")
        # print("FILENAMES", filenames)
        # for filename in filenames:
        #     print(filename)
