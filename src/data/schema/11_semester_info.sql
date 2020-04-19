DROP TABLE IF EXISTS semester_info;
CREATE TABLE semester_info (
    semester varchar(255),
    public boolean,
    PRIMARY KEY (semester)
);

INSERT INTO semester_info (
    SELECT DISTINCT
        c.semester,
        true::boolean
    FROM
        course c
);