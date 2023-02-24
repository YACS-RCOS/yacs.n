CREATE TABLE requriements (
  name_ VARCHAR NOT NULL, 
  classes tsvector ,
  FOREIGN KEY (pathway_id) /*should i use foreign key*/
);