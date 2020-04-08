DROP TABLE IF EXISTS course_prerequisite;
CREATE TABLE course_prerequisite (
    crn varchar(255) REFERENCES course(crn) ON DELETE CASCADE,
    corequisite varchar(255),
    PRIMARY KEY (crn, corequisite)
);