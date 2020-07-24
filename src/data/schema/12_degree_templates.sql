DROP TABLE IF EXISTS degree_templates;
CREATE TABLE degree_templates (
    id          varchar(9),
    degree      varchar(255),
    major       varchar(4),
    year        int,
    semesters   semester,
    PRIMARY KEY (id)
);
