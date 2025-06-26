CREATE TABLE IF NOT EXISTS achivements (
    id integer PRIMARY KEY,
    competition_type_id integer NOT NULL REFERENCES competition_types(id) ON DELETE CASCADE,
    sportsman_id integer NOT NULL REFERENCES sportsmen(id) ON DELETE CASCADE,
    place integer NOT NULL CHECK (place >= 1 AND place <= 3)
)
