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

    def add_professor(self, name, title, email, phone, dep, portfolio, profile_page):
        if email is not None:
            return self.db_conn.execute("""
                INSERT INTO professor (name, title, email, phone_number, department,
                                    portfolio_page, profile_page)
                VALUES (%(name)s, %(title)s, %(email)s, %(phone_number)s, %(department)s,
                        %(portfolio_page)s, %(profile_page)s)
                ON CONFLICT DO NOTHING;
            """, {
                "name": name,
                "title": title,
                "email": email,
                "phone_number": phone,
                "department": dep,
                "portfolio_page": portfolio,
                "profile_page": profile_page,
            })
        else:
            return False, "Email cannot be None."

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

        with open(json_data, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                return False, f"Invalid JSON file: {str(e)}"

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
                                portfolio_page,
                                profile_page
                            )
                            VALUES (
                                NULLIF(%(Name)s, ''),
                                NULLIF(%(Title)s, ''),
                                %(Email)s,
                                NULLIF(%(Department)s, ''),
                                NULLIF(%(Portfolio)s, ''),
                                NULLIF(%(Profile_Page)s, '')
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "Name": entry['Name'],
                                "Title": entry['Title'],
                                "Email": entry['Email'],
                                "Department": entry['Department'],
                                "Portfolio": entry['Portfolio'],
                                "Profile_Page": entry['Profile Page']
                            }
                        )
                    except Exception as e:
                        print(e)
                        conn.rollback()
                        return (False, e)
            except ValueError as ve:
                return (False, "Invalid JSON data: {}".format(ve))

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
