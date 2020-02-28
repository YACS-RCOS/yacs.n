-- -- list of classes offered (all)
select
  c.department,
  c.level,
  max(c.title) as title,
  json_agg(
    row_to_json(section.*)
  ) sections
from
  course c
left join
(
  select
    c1.crn,
    c1.semester,
    max(c1.department) as department,
    max(c1.level) as level,
    json_agg(
      row_to_json(cs.*)
    ) sessions
  from
    course c1
  join course_session cs on
    c1.crn = cs.crn and
    c1.semester = cs.semester
  group by
    c1.crn,
    c1.semester
) section
on
  c.department = section.department and
  c.level = section.level
group by
  c.department,
  c.level
;
-- select
--   c1.crn,
--   c1.semester,
--   c1.department,
--   c1.level,
--   json_agg(
--     row_to_json(cs.*)
--   ) sessions
-- from
--   course c1
-- join course_session cs on
--   c1.crn = cs.crn and
--   c1.semester = cs.semester
-- group by
--   c1.crn,
--   c1.semester,
--   c1.department,
--   c1.level
;
