from sqalchemy import Column, String, Integer
from sqalchemy import relationship
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, DATE, TSVECTOR

from pathways import Pathway
from connection import db
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pathways = relationship("Pathway", back_populates="category")

    #name = Column(VARCHAR(length=255), primary_key=True)
    
    
    #pathways = relationship("Pathway", back_populates="category")
 

    def addPathway(self, pathway_name):
        pathway = Pathway(name=pathway_name, category=self)
        db.execute("INSERT INTO pathways (name, category_id) VALUES (%s, %s)", (pathway.name, pathway.category_id), isSELECT=False)


    def removePathway(self, pathway_name):
        pathway_to_remove = next((pathway for pathway in self.pathways if pathway.name == pathway_name), None)
        if pathway_to_remove:
            db.execute("DELETE FROM pathways WHERE id = %s", (pathway_to_remove.id,), isSELECT=False)