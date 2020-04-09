DROP TABLE IF EXISTS course_prerequisite;
CREATE TABLE course_prerequisite (
    department varchar(255),
    level int,
    prerequisite varchar(255),
    PRIMARY KEY (department, level, prerequisite)
);