-- -- list of classes offered (all)
select
  department,
  level,
  max(title) as title,
  json_agg(crn) as crns
from
  course
group by
  department,
  level
