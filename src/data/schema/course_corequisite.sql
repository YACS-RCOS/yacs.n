DROP TABLE IF EXISTS course_corequisite;
CREATE TABLE course_corequisite (
    department varchar(255),
    level int,
    corequisite varchar(255),
    PRIMARY KEY (department, level, corequisite)
);