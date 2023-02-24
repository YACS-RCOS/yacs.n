CREATE TABLE semester_degree_class (
  semester_id INT NOT NULL, 
  degree_class_id INT NOT NULL,
  PRIMARY KEY (semester_id, degree_class_id),
  /*The semester_id column is a foreign key column that references the id column in the semesters table.*/
  FOREIGN KEY (semester_id) REFERENCES semesters(id),
  FOREIGN KEY (degree_class_id) REFERENCES degree_classes(id)
);
/*https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-table/
#set the primary key to be a combination of semester_id and degree_class_id, 
which ensures that each combination of semester and degree class is unique.
# you can now link each semester to its corresponding degree class, allowing you
 to easily retrieve information about which degree classes were offered during a
  specific semester or which semesters a particular degree class was available.