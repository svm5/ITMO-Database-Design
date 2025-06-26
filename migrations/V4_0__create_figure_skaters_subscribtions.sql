CREATE TABLE IF NOT EXISTS user_figure_skater_subscribes (
    id integer PRIMARY KEY,
    user_account_id integer NOT NULL REFERENCES user_accounts(id) ON DELETE CASCADE,
    sportsman_id integer NOT NULL REFERENCES sportsmen(id) ON DELETE CASCADE,
    created_at timestamp NOT NULL
);

