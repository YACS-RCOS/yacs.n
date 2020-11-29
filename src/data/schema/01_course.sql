--
drop table if exists course;
create table course(
  crn           varchar(255),
  section       varchar(255),
  semester      varchar(255),
  min_credits   int,
  max_credits   int,
  date_start    date,
  date_end      date,
  department    varchar(255),
  level         int,
  title         varchar(255),
  full_title    text,
  description   text,
  raw_precoreqs text,
  frequency     varchar(255),
  school        varchar(255),
  seats_open    int,
  seats_filled  int,
  seats_total   int,
  tsv           tsvector,
  primary key (crn)
);
