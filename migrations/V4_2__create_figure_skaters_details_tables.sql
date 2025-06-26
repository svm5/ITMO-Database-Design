CREATE TABLE IF NOT EXISTS figure_skaters_nicknames (
    id integer PRIMARY KEY,
    nickname varchar(100) NOT NULL,
    sportsman_id integer NOT NULL REFERENCES sportsmen(id) ON DELETE CASCADE,
    bears_amount integer NOT NULL CHECK (bears_amount >= 0)
);

CREATE TABLE IF NOT EXISTS figure_skaters_photos (
    id integer PRIMARY KEY,
    photo varchar(500) NOT NULL,
    sportsman_id integer NOT NULL REFERENCES sportsmen(id) ON DELETE CASCADE,
    bears_amount integer NOT NULL CHECK (bears_amount >= 0)
);

CREATE TABLE IF NOT EXISTS notes (
    id integer PRIMARY KEY,
    user_account_from_id integer NOT NULL REFERENCES user_accounts(id) ON DELETE CASCADE,
    sportsman_id integer NOT NULL REFERENCES sportsmen(id) ON DELETE CASCADE,
    note_text varchar(300) NOT NULL,
    created_at timestamp NOT NULL,
    bears_amount integer NOT NULL CHECK (bears_amount >= 0)
);

CREATE TABLE IF NOT EXISTS hidden_notes (
    id integer PRIMARY KEY,
    user_account_id integer NOT NULL REFERENCES user_accounts(id) ON DELETE CASCADE,
    note_id integer NOT NULL REFERENCES notes(id) ON DELETE CASCADE
)
