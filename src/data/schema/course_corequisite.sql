DROP TABLE IF EXISTS course_corequisite;
CREATE TABLE course_corequisite (
    crn varchar(255) REFERENCES course(crn) ON DELETE CASCADE,
    corequisite varchar(255),
    PRIMARY KEY (crn, corequisite)
);