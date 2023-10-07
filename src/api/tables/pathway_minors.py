from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

import json

#from .database import Base

class pathway_minors():
    __tablename__ = "pathway_minors"

    pathway = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    minor  = Column(VARCHAR(length=255), primary_key = True, nullable=False)



# def load_minors(data):
#     for i in data:
#         for p in i['Pathways']:
#             if 'Compatible minor(s)' in p.keys():
#                 for minor in p['Compatible minor(s)']:
#                     print(minor)
#                     print(p['Name'][0])
#
# if __name__ == "__main__":
#     with open('../../web/src/pages/pathwayV2.json') as file:
#         data = json.load(file)
#     load_minors(data)
#
#     # fields = dict()
#     # for i in data:
#     #     #print(i)
#     #     for pathway in i['Pathways']:
#     #         #print(pathway.keys())
#     #         if 'Compatible minor(s)' in pathway.keys():
#     #             print(pathway['Compatible minor(s)'])
#     #             print(pathway['Name'])
#         # for j in data[i]:
#         #     print(' ', j)
