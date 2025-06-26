CREATE TABLE IF NOT EXISTS single_figure_skaters (
    id integer PRIMARY KEY,
    name varchar(200) NOT NULL,
    bears_amount integer NOT NULL CHECK (bears_amount >= 0),
    photo varchar(500) NOT NULL,
    country varchar(200) NOT NULL,
    birthday DATE NOT NULL,
    nickname varchar(200),
    category_id integer REFERENCES categories(id) ON DELETE SET NULL,
    is_career_active boolean
);

CREATE TABLE IF NOT EXISTS figure_skater_pairs (
    id integer PRIMARY KEY,
    woman_name varchar(200) NOT NULL,
    man_name varchar(200) NOT NULL,
    bears_amount integer NOT NULL CHECK (bears_amount >= 0),
    photo varchar(500) NOT NULL,
    country varchar(200) NOT NULL,
    woman_birthday DATE NOT NULL,
    man_birthday DATE NOT NULL,
    nickname varchar(200),
    category_id integer REFERENCES categories(id) ON DELETE SET NULL,
    is_career_active boolean
);

CREATE TABLE IF NOT EXISTS sportsmen (
    id integer PRIMARY KEY,
    figure_skater_id integer NOT NULL,
    figure_skater_type varchar(100) NOT NULL
);
