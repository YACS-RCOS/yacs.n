drop table if exists admin_settings;
create table admin_settings(
  semester varchar(255)
);

INSERT INTO admin_settings (semester)
VALUES (
  (SELECT semester FROM course LIMIT 1)
);
