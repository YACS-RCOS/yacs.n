-- Adminer 4.7.6 PostgreSQL dump

DROP TABLE IF EXISTS "popular_courses";
CREATE TABLE "public"."popular_courses" (
    "Course_code" text NOT NULL,
    "Course_name" text NOT NULL,
    "Popularity" INT NOT NULL,
        PRIMARY KEY ("Course_name")
) WITH (oids = false);