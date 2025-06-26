CREATE TABLE IF NOT EXISTS bears_account_transactions (
    id integer PRIMARY KEY,
    user_account_id integer NOT NULL REFERENCES user_accounts(id) ON DELETE CASCADE,
    bears_amount integer NOT NULL CHECK(bears_amount > 0),
    transaction_type varchar(100) NOT NULL,
    comment varchar(256) DEFAULT '' NOT NULL,
    created_at timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS bears_transfer_transactions (
    id integer PRIMARY KEY,
    user_account_from_id integer NOT NULL REFERENCES user_accounts(id) ON DELETE CASCADE,
    sportsman_id integer NOT NULL REFERENCES sportsmen(id) ON DELETE CASCADE,
    bears_amount integer NOT NULL CHECK(bears_amount > 0),
    comment varchar(256) DEFAULT '' NOT NULL,
    created_at timestamp NOT NULL
)

