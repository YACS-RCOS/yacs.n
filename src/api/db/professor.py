import json
from psycopg2.extras import RealDictCursor
import asyncio
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from your_module import Professor, Base

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection

class Professor:
    
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def add_professor(self, first_name, last_name, email, phone, dep, office, 
        classes, office_time, rcs):
            if email is not None:
                print(email)
                return self.db_conn.execute("""
            INSERT INTO 
                professor (first_name, last_name, email, phone_number, 
                department, office_room, classes, office_hours_time, rcs)
            VALUES 
                   (%(First_name)s, %(Last_name)s, %(Phone_number)s, %(Email)s,
                   %(Dep)s, %(Office_room)s, %(Classes)s, %(Office_time)s, %(Rcs_id)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "First_name": first_name,
                "Last_name": last_name,
                "Email": email, 
                "Phone_number": phone,
                "Dep": dep, 
                "Office_room": office, 
                "Classes": classes,
                "Office_time": office_time,
                "Rcs_id": rcs
            }
        , False)
            else:
                return (False, "email cant be none")

    def add_bulk_professor(self):
        # Load the JSON data from a file
        with open('Professors.json') as file:
            data = json.load(file)

        # Connect to the SQL database
        conn = self.db.get_connection()

        # Loop through each professor record in the JSON data
        for record in data:
            professor = Professor(email=record['Email'],
                                first_name=record['Name'],
                                phone_number=record['Phone'],
                                department=record['Department'],
                                office_room=record['Portfolio'],
                                office_hours_time='',
                                rcs='')
            conn.add(professor)

        # Commit the changes to the database
        conn.commit()
        self.clear_cache()
        return (True,None)

    def populate_from_json(self, json_data):
        # Connect to the database
        conn = self.db_conn.get_connection()

        # Read JSON data
        data = json.loads(json_data)

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                for entry in data:
                    try:
                        # Professors
                        transaction.execute(
                            """
                            INSERT INTO professor (
                                name,
                                title,
                                email,
                                department,
                                portfolio_page
                            )
                            VALUES (
                                NULLIF(%(Name)s, ''),
                                NULLIF(%(Title)s, ''),
                                %(Email)s,
                                NULLIF(%(Department)s, ''),
                                NULLIF(%(Portfolio_page)s, '')
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "Name": entry['Name'],
                                "Title": entry['Title'],
                                "Email": entry['Email'],
                                "Department": entry['Department'],
                                "Portfolio_page": entry['Portfolio']
                            }
                        )
                    except Exception as e:
                        print(e)
                        conn.rollback()
                        return (False, e)
            #except statement
            except ValueError as ve:
                return (False, "Invalid JSON data: {}".format(ve))

        conn.commit()
        # Invalidate cache so we can get new classes
        self.clear_cache()
        return (True, None)

    #removes professor if it exists
    def remove_professor(self, email):
        if email is not None:
            sql = """
                DELETE FROM 
                    professor
                WHERE
                    email = '{email}'
                """
            error = self.db_conn.execute(sql, None, False)
        else:
            return (False, "email cant be none")
        return (True, None)

    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))

    def bulk_delete(self,professors):
        for professor in professors:
            _, error = self.remove_professor(professor)
            if error:
                print(error)
                return error
        # on success, invalidate cache
        self.clear_cache()
        return None

    # if you expect the SQL statement to return more than one row of data, you should pass True as the value for multi.
    def get_professor_info_by_email(self, email):
        if email is not None:
            sql = """
                    select
                        *
                    from
                        professor
                    where
                        email = '%s'
                    """ % email
        info, error = self.db_conn.execute(sql, None, True)
        return (info, None) if not error else (False, error)

    def get_professor_phone_number_by_email(self, email):
        if email is not None:
            sql = """
                    select
                        phone_number
                    from
                        professor
                    where
                        email = '%s'
                    """ % email
        phone_number, error = self.db_conn.execute(sql, None, True)
        return (phone_number, None) if not error else (False, error)
    
    def get_professor_info_by_rcs(self,rcs):
        return self.get_professor_info_by_email(rcs+"@rpi.edu")

    def get_professor_rcs_by_email(self,email):
        if email is not None:
            sql = """
                    select
                        rcs
                    from
                        professor
                    where
                        email = '%s'
                    """ % email
        rcs, error = self.db_conn.execute(sql, None, True)
        return (rcs, None) if not error else (False, error)

    def get_office_hours_by_email(self,email):
        if email is not None:
            sql = """
                    select
                        office_room
                        office_hours_time
                    from
                        professor
                    where
                        email = '%s'
                    """ % email
        office_hours, error = self.db_conn.execute(sql, None, True)
        return (office_hours,error) if not error else (False,error)

    #return as a json
    def get_all_professors(self):  
        return self.db_conn.execute(""" 
                            SELECT * FROM professor
                    """, None, True)
    
    #gets prfoessors' phone number by their email
    def get_professor_phone_number_by_email(self, email):
        if email is not None:
            sql = """
                    select
                        phone_number
                    from
                        professor
                    where
                        email = '%s'
                    """ % email
            phone_number, error = self.db_conn.execute(sql, None, True)
            return (phone_number, None) if not error else (False, error)

    def get_professor_name_by_email(self, email):
        if email is not None:
            sql = """
                    select
                        first_name,
                        last_name
                    from
                        professor
                    where
                        email = '%s'
                    """ % email
            name, error = self.db_conn.execute(sql, None, True)
            return (name, None) if not error else (False, error)


    #seraches professors who are in a certain department
    def get_professors_by_department(self,department): 
        sql = """
                select
                    *
                from
                    professor
                where
            department = '%s'
        """ % department
        department, error = self.db_conn.execute(sql, None, True)
        return (department, None) if not error else (False, error)

if __name__ == "__main__":
    csv_text = open('../../../rpi_data/fall-2020.csv', 'r')
    courses = Professor(connection.db)
    courses.populate_from_csv(csv_text)
