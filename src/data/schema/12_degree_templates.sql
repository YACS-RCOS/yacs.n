DROP TABLE IF EXISTS degree_templates;

CREATE TABLE degree_templates (
    id          varchar(255),
    degree      varchar(255),
    major       varchar(255),
    year        int,
    semesters1   varchar(255),/*ITWS_2018_sm1 */
    semesters2   varchar(255),
    semesters3   varchar(255),
    semesters4   varchar(255),
    semesters5   varchar(255),
    semesters6   varchar(255),
    semesters7   varchar(255),
    semesters8   varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE degree_templates_semester (
    course1 varchar(255),
    course2 varchar(255),
    course3 varchar(255),
    course4 varchar(255),
    course5 varchar(255),
    semestersName   varchar(255),
    PRIMARY KEY (semestersName)
);

CREATE TABLE degree_option_course (
    name varchar(255),
    description varchar(255),
    id varchar(255),
    PRIMARY KEY (name)
);