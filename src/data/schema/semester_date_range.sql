DROP TABLE IF EXISTS semester_date_range;
CREATE TABLE semester_date_range (
    semester_name varchar(255),
    date_start date,
    date_end date
);

INSERT INTO semester_date_range (semester_name, date_start, date_end) (
    SELECT DISTINCT
        semester || ' (' || ((date_end - date_start)/7)::text || ')',
        date_start,
        date_end
    FROM
        course
);