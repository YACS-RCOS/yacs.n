from sqlalchemy import Column, ForeignKey
from sqalchemy import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, TSVECTOR

from .database import Base

if __name__ == "__main__":
    import connection
else:
    from . import connection

class Pathway(Base):
    __tablename__ = "pathway"

    name = Column(VARCHAR(length=255), primary_key=True)
    description = Column(TEXT)
    compatible_minor = Column(VARCHAR(length=255))
    category_name = Column(VARCHAR(length=255), ForeignKey('categories.name'))

    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def addPathway(self, pathway_name, courses):
            if pathway_name is not None:
                print(pathway_name)
                return self.db_conn.execute("""
            INSERT INTO
                pathways (pathway_name, courses)
            VALUES 
                   (%(Pathway_name)s, %(Courses)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "Pathway_name": pathway_name,
                "courses": courses,
            }
        , False)
            else:
                return (False, "pathway cant be none")
            
    def addCourse(self, pathway_name, courses):
            if courses is not None:
                print(courses)
                return self.db_conn.execute("""
            INSERT INTO 
                pathways (pathway_name, courses)
            VALUES 
                   (%(Pathway_name)s, %(Courses)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "Pathway_name": pathway_name,
                "courses": courses,
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
    
    def removeCourse(self, pathway_name, courses):
        if courses is not None:
            sql = """
                DELETE FROM 
                    pathways
                WHERE
                    courses = '{courses}'
                """
            error = self.db_conn.execute(sql, None, False)
        else:
            return (False, "course cant be none")
        return (True, None)

    def getPathway(self, courses):
        if courses is not None:
            sql = """
                    select
                        *
                    from
                        pathways
                    where
                courses = '%s'
            """ 
        courses, error = self.db_conn.execute(sql, (courses,), True)
        return (courses, None) if not error else (False, error)
    
    def getCourse(self, pathway_name):
        if pathway_name is not None:
            sql = """
                    select
                        *
                    from
                        pathways
                    where
                pathway_name = '%s'
            """
        pathway__name, error = self.db_conn.execute(sql, (pathway_name,), True)
        return (pathway_name, None) if not error else (False, error)
    
    course = relationship("Course", back_populates="pathway")
    category_name = Column(VARCHAR(length=255), ForeignKey('categories.name'))
    category = relationship("Category", back_populates="pathways")