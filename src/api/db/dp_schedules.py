from db.model import *
import json

class Dp_schedules:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def update(self, schedule_id, selected_classes, degree):
        """
        Create a new entry or update the values of an existing entry.
        """
        # Serialize the Python object to a JSON string
        selected_classes_json = json.dumps(selected_classes)
        
        # Upsert the data into the database
        _, error = self.db_conn.execute("""
            INSERT INTO dp_schedules (schedule_id, selected_classes, degree) VALUES (%s, %s, %s)
            ON CONFLICT (schedule_id) 
            DO UPDATE SET selected_classes = EXCLUDED.selected_classes, degree = EXCLUDED.degree
        """, (schedule_id, selected_classes_json, degree))
        return (True, None) if not error else (False, error)

    def delete(self, schedule_id):
        """
        Delete an entry based on the schedule_id.
        """
        # Delete the data from the database
        _, error = self.db_conn.execute("DELETE FROM dp_schedules WHERE schedule_id = %s", (schedule_id,))
        return (True, None) if not error else (False, error)
    
    def get_schedule(self, schedule_id):    
        result, error = self.db_conn.execute("SELECT schedule_id, selected_classes, degree FROM dp_schedules WHERE schedule_id = %s", (schedule_id,))

        if result is None:
            return (False, None)

        schedule_id, selected_classes, degree = result
        return ({
            'schedule_id': schedule_id,
            'selected_classes': json.loads(selected_classes) if selected_classes else None,
            'degree': degree
        }, None) if not error else (False, error)
