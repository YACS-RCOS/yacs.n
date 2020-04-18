--
drop table if exists course;
create table course(
  crn          varchar(255),
  section      varchar(255),
  semester     varchar(255),
  date_start   date,
  date_end     date,
  department   varchar(255),
  level        int,
  title        varchar(255),
  full_title   text,
  description  text,
  raw_precoreqs text,
  frequency    varchar(255),
  -- credit_hours int,
  -- class_days varchar(255),
  -- instructor varchar(255),
  -- seats_available varchar(255),
  -- seats_filled varchar(255),
  primary key (crn)
);
