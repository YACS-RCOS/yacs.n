-- find sessions from a set of (crn, semester)
select
  c.title,
  c.date_start,
  c.date_start,
  cs.day_of_week,
  cs.time_start,
  cs.time_end
from
  course c
join course_session cs on
  cs.crn = c.crn and
  cs.semester = c.semester and
  cs.section = c.section
where
  c.crn in ('15343', '15340') and
  c.semester = 'SUMMER 2020'
