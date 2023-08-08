from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, TSVECTOR

from .database import Base

if __name__ == "__main__":
    import connection
else:
    from . import connection

class Pathway(Base):
    __tablename__ = "pathway"

    name = Column(VARCHAR(length=255))
    description = TEXT
    required_courses = Column(TSVECTOR, bool = False)
    #foreign key for courses
    courses = Column(TSVECTOR, ForeignKey("course.crn"))
    compatible_minor = Column(TSVECTOR)

    category_name = Column(VARCHAR(length=255), ForeignKey('categories.name'))

    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def addPathway(self, pathway_name, course_name):
            if pathway_name is not None:
                print(pathway_name)
                return self.db_conn.execute("""
            INSERT INTO 
                #course_name -> category_name??
                pathways (pathway_name, course_name)
            VALUES 
                   (%(Pathway_name)s, %(Course_name)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "Pathway_name": pathway_name,
                "Course_name": course_name,
            }
        , False)
            else:
                return (False, "pathway cant be none")
            
    def addCourse(self, pathway_name, course_name):
            if course_name is not None:
                print(course_name)
                return self.db_conn.execute("""
            INSERT INTO 
                pathways (pathway_name, course_name)
            VALUES 
                   (%(Pathway_name)s, %(Course_name)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "Pathway_name": pathway_name,
                "Course_name": course_name,
            }
        , False)
            else:
                return (False, "course cant be none")
            
    def removePathway(self, pathway_name):
        if pathway_name is not None:
            sql = """
                DELETE FROM 
                    pathways
                WHERE
                    pathway_name = '{pathway_name}'
                """
            error = self.db_conn.execute(sql, None, False)
        else:
            return (False, "pathway cant be none")
        return (True, None)
    
    def removeCourse(self, pathway_name, course_name):
        if course_name is not None:
            sql = """
                DELETE FROM 
                    pathways
                WHERE
                    course_name = '{course_name}'
                """
            error = self.db_conn.execute(sql, None, False)
        else:
            return (False, "course cant be none")
        return (True, None)

    def getPathway(self, course_name):
        if course_name is not None:
            sql = """
                    select
                        pathway_name
                    from
                        pathways
                    where
                        course_name = '%s'
                    """ % course_name
        pathway_name, error = self.db_conn.execute(sql, None, True)
        return (pathway_name, None) if not error else (False, error)
    
    def getCourse(self, pathway_name):
        if pathway_name is not None:
            sql = """
                    select
                        course_name
                    from
                        pathways
                    where
                        pathway_name = '%s'
                    """ % pathway_name
        course_name, error = self.db_conn.execute(sql, None, True)
        return (course_name, None) if not error else (False, error)