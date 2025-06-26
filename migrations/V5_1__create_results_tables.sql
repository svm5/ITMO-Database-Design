CREATE TABLE IF NOT EXISTS competition_results (
    id integer PRIMARY KEY,
    participant_id integer NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    points float NOT NULL CHECK(points >= 0)
);

CREATE TABLE IF NOT EXISTS perfomance_results (
    id integer PRIMARY KEY,
    participant_id integer NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    perfomance_type_id integer REFERENCES perfomance_types(id) ON DELETE SET NULL,
    technical_elements_points float NOT NULL CHECK (technical_elements_points >= 0),
    components_points float NOT NULL CHECK (components_points >= 0),
    deductions float NOT NULL DEFAULT '0' CHECK (deductions >= 0)
);

CREATE TABLE IF NOT EXISTS components_details (
    id integer PRIMARY KEY,
    perfomance_result_id integer NOT NULL REFERENCES perfomance_results(id) ON DELETE CASCADE,
    skating_skills_points float NOT NULL CHECK (skating_skills_points >= 0),
    transitions_points float NOT NULL CHECK (transitions_points >= 0),
    perfomance_points float NOT NULL CHECK (perfomance_points >= 0),
    composition_points float NOT NULL CHECK (composition_points >= 0),
    interpretation_points float NOT NULL CHECK (interpretation_points >=0)
);

CREATE TABLE IF NOT EXISTS technical_elements_names (
    id integer PRIMARY KEY,
    name varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS technical_elements_marks (
    id integer PRIMARY KEY,
    name varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS technical_elements_results (
    id integer PRIMARY KEY,
    perfomance_result_id integer NOT NULL REFERENCES perfomance_results(id) ON DELETE CASCADE,
    number integer NOT NULL CHECK (number >= 0),
    element_name_id integer NOT NULL REFERENCES technical_elements_names(id) ON DELETE CASCADE,
    element_mark_id integer NOT NULL REFERENCES technical_elements_marks(id) ON DELETE CASCADE,
    base_value float NOT NULL CHECK (base_value > 0),
    goe float NOT NULL CHECK(goe >= -5 AND goe <= 5)
)
