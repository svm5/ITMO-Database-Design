CREATE TABLE IF NOT EXISTS user_accounts (
    id integer PRIMARY KEY,
    name varchar(200) NOT NULL,
    short_description varchar(300),
    email varchar(100) NOT NULL,
    bears_amount integer NOT NULL CHECK (bears_amount >= 0),
    city_id integer REFERENCES cities(id) ON DELETE SET NULL,
    photo varchar(500),
    last_login timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS user_secrets (
    id integer PRIMARY KEY REFERENCES user_accounts(id),
    password varchar(100) NOT NULL
);

