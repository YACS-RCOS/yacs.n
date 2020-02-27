--
-- course/sections --
insert into course
values
  -- full semester courses
  (15343, 01, 'SUMMER 2020', '2020-05-26', '2020-10-21', 'ARCH', '2510', 'MATERIALS AND DESIGN'),
  (15344, 02, 'SUMMER 2020', '2020-05-26', '2020-10-21', 'ARCH', '2510', 'MATERIALS AND DESIGN'),
  (15329, 01, 'SUMMER 2020', '2020-05-26', '2020-10-21', 'COGS', '4360', 'BEHAVIOURAL NEUROSCIENCE'),
  -- first half semester courses
  (12312, 01, 'SUMMER 2020', '2020-05-26', '2020-07-10', 'ARCH', '2520', 'DIGITAL CONSTRUCTS 1'),
  (15340, 01, 'SUMMER 2020', '2020-05-26', '2020-07-10', 'BIOL', '4200', 'BIOSTATISTICS'),
  -- second half semester courses
  (15272, 01, 'SUMMER 2020', '2020-07-10', '2020-10-21', 'ARCH', '2530', 'DIGITAL CONSTRUCTS 2'),
  (15694, 01, 'SUMMER 2020', '2020-07-10', '2020-10-21', 'ARTS', '2968', 'MUSIC, AFFECT & EMBOD LISTEN');
  -- course/sections --
  insert into course_session
  values
    -- materials (01)
    (15343, 01, 'SUMMER 2020', '10:00AM', '11:50AM', '0'),
    (15343, 01, 'SUMMER 2020', '10:00AM', '11:50AM', '3'),

    -- materials (02)
    (15344, 02, 'SUMMER 2020', '12:00PM', '1:50PM', '1'),
    (15344, 01, 'SUMMER 2020', '12:00PM', '1:50PM', '4'),

    -- biostatistics
    (15340, 01, 'SUMMER 2020', '12:00PM', '1:50PM', '3'),
    (15340, 01, 'SUMMER 2020', '12:00PM', '1:50PM', '0');

    -- -- first half semester courses
    -- (12312, 01, 'SUMMER 2020', '10:00AM', '11:50AM', '0'),
    -- (15340, 01, 'SUMMER 2020', '10:00AM', '11:50AM', '0'),
    -- -- second half semester courses
    -- (15272, 01, 'SUMMER 2020', '10:00AM', '11:50AM', '0'),
    -- (15694, 01, 'SUMMER 2020', '10:00AM', '11:50AM', '0'),
;
