CREATE TABLE IF NOT EXISTS competitions (
    id integer PRIMARY KEY,
    name varchar(256) NOT NULL,
    city_id integer NOT NULL REFERENCES cities(id) ON DELETE SET NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    competition_type_id integer REFERENCES competition_types(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS participants  (
    id integer PRIMARY KEY,
    competition_id integer NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
    sportsman_id integer NOT NULL REFERENCES sportsmen(id) ON DELETE CASCADE,
    category_id integer NOT NULL REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS prediction_contests (
    id integer PRIMARY KEY,
    competition_id integer NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
    category_id integer NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    is_active boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS user_predictions (
    id integer PRIMARY KEY,
    user_account_id integer NOT NULL REFERENCES user_accounts(id) ON DELETE CASCADE,
    participant_id integer NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    place integer NOT NULL CHECK (place >= 1 AND place <= 3)
);
