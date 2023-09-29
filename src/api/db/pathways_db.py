import csv
import json
from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from your_module import Professor, Base

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
# if __name__ == "__main__":
#     import connection
# else:
#     from . import connection


class Pathway:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    # def add_professor(self, first_name, last_name, email, phone, dep, office,
    #     classes, office_time, rcs):
    #         if email is not None:
    #             print(email)
    #             return self.db_conn.execute("""
    #         INSERT INTO
    #             professor (first_name, last_name, email, phone_number,
    #             department, office_room, classes, office_hours_time, rcs)
    #         VALUES
    #                (%(First_name)s, %(Last_name)s, %(Phone_number)s, %(Email)s,
    #                %(Dep)s, %(Office_room)s, %(Classes)s, %(Office_time)s, %(Rcs_id)s)
    #         ON CONFLICT DO NOTHING
    #         ;
    #     """, {
    #             "First_name": first_name,
    #             "Last_name": last_name,
    #             "Email": email,
    #             "Phone_number": phone,
    #             "Dep": dep,
    #             "Office_room": office,
    #             "Classes": classes,
    #             "Office_time": office_time,
    #             "Rcs_id": rcs
    #         }
    #     , False)
    #         else:
    #             return (False, "email cant be none")



def add_bulk_professor():
    # Load the JSON data from a file
    with open('../../../src/web/src/pages/pathwayV2.json') as file:
        data = json.load(file)

    # Connect to the SQL database
    #conn = self.db.get_connection()

    # Loop through each professor record in the JSON data
    for category in data:
        category_name = category["Category Name"][0]
        print(f"Category Name: {category_name}")

        for pathway in category["Pathways"]:
            pathway_name = pathway["Name"][0]
            print(f"Pathway Name: {pathway_name}")

            choose_one = pathway["Choose one of the following"]
            choose_remaining = pathway["Choose remaining credits from the following"]

            print("Choose one of the following:")
            for course in choose_one:
                print(f"- {course}")

            print("Choose remaining credits from the following:")
            for course in choose_remaining:
                print(f"- {course}")

            compatible_minors = pathway.get("Compatible minor(s)")
            if compatible_minors:
                print("Compatible minor(s):", ", ".join(compatible_minors))

            print("\n")
        #conn.add(professor)

    # Commit the changes to the database
    #onn.commit()
    #self.clear_cache()
    return (True,None)



# if __name__ == "__main__":
#     csv_text = open('../../../src/web/src/pages/pathwayV2.json', 'r')
#     pathways = Pathway(connection.db)
#     pathways.populate_from_csv(csv_text)

add_bulk_professor()
