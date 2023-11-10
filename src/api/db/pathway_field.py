import csv
import json
from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


##!!!!!!!!!!!!!!!!!!!!
## TO UPDATE WITH NEW PATHWAYS/CATEGORIES, CHANGE JSON FILE AT BOTTOM OF PAGE
##!!!!!!!!!!!!!!!!!!!!

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection


class Pathway_Field:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    # def add_field(self, pathway_name, course_name, field_name, occurrence):
    #     if pathway_name is not None and course_name is not None:
    #         return self.db_conn.execute("""
    #         INSERT INTO
    #             pathway (pathway_name, course_name, field_name, occurrence)
    #         VALUES
    #                (%(pathway_name)s, %(course_name)s, %(field_name)s, %(occurrence)s)
    #         ON CONFLICT DO NOTHING
    #         ;
    #     """, {
    #             "pathway_name": pathway_name,
    #             "course_name": course_name,
    #             "field_name": field_name,
    #             "occurrence": occurrence
    #         }, False)
    #     else:
    #         return (False, "pathway_name and course_name cannot be none")

    def add_bulk_fields(self, json_data): #function is called in app.py
        # Connect to the SQL database
        conn = self.db_conn.get_connection()

        fields = dict()
        fields['Choose one of the following'] = 'Choose one of the following'
        fields['Choose another one of the following'] = 'Choose one of the following'
        fields['Can select only one of the following to be applied to pathway'] = 'Choose one of the following'
        fields['Choose 12 credits from the following'] = 'Choose 12 credits from the following'

        fields['Choose 12 credits from the following course prefixes, ' \
              'with at least 8 credit hours at, or above, ' \
              'the 2000-level and at least 3 credit hours at the 4000-level'] = \
                'Choose 12 credits from the following course prefixes, ' \
              'with at least 8 credit hours at, or above, ' \
              'the 2000-level and at least 3 credit hours at the 4000-level'

        fields['Choose 12 credits from the following, with at least 4 credits at the 4000-level'] =\
            'Choose 12 credits from the following, with at least 4 credits at the 4000-level'

        fields['Choose 4 credits from the following'] = 'Choose 4 credits from the following'
        fields['Choose remaining credits from the following'] = 'Choose remaining credits from the following'

        fields['Choose remaining credits from the following, with at least 4 credits at the 4000-level'] = \
            'Choose remaining credits from the following, with at least 4 credits at the 4000-level'

        fields['Required'] = 'Required'

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                # Iterate over each entry in the JSON data
                transaction.execute(
                    """
                    DELETE FROM pathway_field;
                    """
                )

                for entry in json_data:
                    for sub in entry['Pathways']:
                        occurrence = dict()
                        for title in sub.keys():
                            if title != 'Name' and title != 'Compatible minor(s)':
                                field = fields[title] # Ex. Required, Choose x...
                                if field not in occurrence:
                                    occurrence[field] = 1
                                else:
                                    occurrence[field] += 1
                                for course in sub[title]:
                                    try:
                                        # Fetch course_credits from course_master database using course_name
                                        # course_credits = 0  # Default value if not found
                                        # # Query the course_master database to get max_credits for the current course
                                        # query = "SELECT max_credits FROM course_master WHERE title = '% ',%s,' %';"
                                        # transaction.execute(query, (course,))
                                        # result = transaction.fetchone()
                                        # if result:
                                        #     course_credits = result['max_credits'

                                        # Insert pathways and corresponding category into "pathway" table (tables/pathways.py)
                                        transaction.execute(
                                            """
                                            INSERT INTO pathway_field (
                                                pathway_name,
                                                course_name,
                                                field_name,
                                                occurrence,
                                                course_credits
                                            )
                                            VALUES (
                                                NULLIF(%(pathway_name)s, ''),
                                                NULLIF(%(course_name)s, '') ,
                                                NULLIF(%(field_name)s, ''),
                                                NULLIF(%(occurrence)s, ''),
                                                NULLIF(%(course_credits)s, -2)
                                            )
                                            ON CONFLICT DO NOTHING;
                                            """,
                                            {
                                                "pathway_name": sub['Name'][0],
                                                "course_name": course,
                                                "field_name": field,
                                                "occurrence": str(occurrence[field]),
                                                "course_credits": -2
                                            }
                                        ),
                                        transaction.execute(
                                            """
                                            UPDATE pathway_field SET course_credits = (
                                                SELECT cm.max_credits
                                                FROM course_master cm
                                                JOIN pathway_field pf on pf.course_name = cm.title
                                            )
                                            """
                                        )
                                    except Exception as e:
                                        # Roll back the transaction and return the exception if an error occurs
                                        print("THIS IS THE EXCEPTION: pathway_fields", e)
                                        conn.rollback()
                                        return (False, e)
            except ValueError as ve:
                # Return an error message if the JSON data is invalid
                return (False, f"Invalid JSON data: {str(ve)}")

            # Commit the transaction if all entries are inserted successfully
            conn.commit()

            # Invalidate cache to ensure new data is retrieved
            self.clear_cache()

            # Return success status and no error
            return True, None

    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))


if __name__ == "__main__":
    field = Pathway_Field(connection.db)
    field.add_bulk_fields('../../../src/web/src/pages/pathwayV2.json') #CHANGE FILE HERE IF NEEDED
