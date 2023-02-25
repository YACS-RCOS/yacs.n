CREATE TABLE requriements (
  name_ VARCHAR NOT NULL, 
  classes tsvector , /*choose one of the following: */
  num_classes_needed INT , /*not sure if needed */
  FOREIGN KEY (pathway_id) /*should i use reference*/
);

/*
name: not sure what to put
classes:                 
    "IHSS 1960 - Remixing in Digital Culture",
    "IHSS 1960 - Worlds on Display",
    "IHSS 1960 - Game Sound and Musical Play",
    "ARTS 1020 - Digital Imaging",
    and more
num_classes_needed: 3
pathway_id: "creatie design and innovation"
*/