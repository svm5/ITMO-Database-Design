CREATE TABLE IF NOT EXISTS categories (
    id integer PRIMARY KEY,
    name varchar(200) NOT NULL
);


CREATE TABLE IF NOT EXISTS competition_types (
    id integer PRIMARY KEY,
    name varchar(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS perfomance_types (
    id integer PRIMARY KEY,
    name varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    id integer PRIMARY KEY,
    country varchar(256) NOT NULL,
    city varchar(256) NOT NULL
);

