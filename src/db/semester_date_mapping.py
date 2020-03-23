class semester_date_mapping:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def insert(self, date_start, date_end, name):
        return self.db.execute("""
            INSERT INTO semester_date_range (semester_part_name, date_start, date_end)
            VALUES (%(SemesterPartName)s, %(DateStart)s, %(DateEnd)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
            "SemesterPartName": name,
            "DateStart": date_start,
            "DateEnd": date_end
        }, isSELECT=False)