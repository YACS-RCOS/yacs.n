-- list of classes offered (all)
select
  distinct concat(c.department, '-', c.level) as class,
  cd.title
from
  (
    select
      department, level
    from
      course
    group by
      department,
      level
  ) c
join course cd on
  c.department = cd.department and
  c.level = cd.level
