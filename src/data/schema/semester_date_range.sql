DROP TABLE IF EXISTS semester_date_range;
CREATE TABLE semester_date_range (
    semester_part_name varchar(255),
    date_start date,
    date_end date,
    PRIMARY KEY (date_start, date_end)
);

INSERT INTO semester_date_range (semester_part_name, date_start, date_end) (
    SELECT DISTINCT
        TO_CHAR(date_start, 'MM/DD') || '-' || TO_CHAR(date_end, 'MM/DD'),
        date_start,
        date_end
    FROM
        course
);