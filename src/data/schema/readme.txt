(thinking about the data here:)

/*

class has sessions during a week
- if a class is offered over total term, it belongs to all semester_parts for that semester
- if a class is offered over half term, then it only belongs to that semester part

class(
  crn,
  section,
  semester,
  date_start,
  date_end,
  title,
  credit_hours,
  class_days,
  instructor,
  seats_available,
  seats_filled
)

class_session(
  crn,
  section,
  semester,
  time_start,
  time_end,
  day_of_week, (0-7)
)

ignore for now
seats(
  crn,
  semester,
  available,
  filled
);

class is offered in multop

*/

-- example class: (15343, 'summer 2020', 'architelj..', )
