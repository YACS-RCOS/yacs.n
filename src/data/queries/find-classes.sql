-- -- list of classes offered (all)
select
  c.department,
  c.level,
  max(c.title) as title,
  json_agg(
    row_to_json(c1.*)
  ) courses
from
  course c
join course c1 on
  c.department = c1.department and
  c.level = c1.level
group by
  c.department,
  c.level
