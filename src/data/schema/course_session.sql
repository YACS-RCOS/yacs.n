--
-- session is like a block on your calendar.
-- i.e. CSCI-1200 on Tuesday at 10AM to 11:50

drop table course_session;
create table course_session(
  crn varchar(255),
  section varchar(255),
  semester varchar(255),
  time_start time,
  time_end time,
  day_of_week int,
  location varchar(255),
  PRIMARY KEY (
    crn,
    section,
    semester,
    day_of_week
  )
);
