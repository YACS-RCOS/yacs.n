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

    def insert_all(self, start_dates, end_dates, names):
        if len(start_dates) == len(end_dates) == len(names):
            for i in range(len(start_dates)):
                if (names[i] and not names[i].isspace()):
                    # https://stackoverflow.com/questions/36886134/postgres-conflict-handling-with-multiple-unique-constraints
                    _, error = self.db.execute("""
                        INSERT INTO semester_date_range (semester_part_name, date_start, date_end)
                        VALUES (%(SemesterPartName)s, %(DateStart)s, %(DateEnd)s)
                        ON CONFLICT ON CONSTRAINT semester_date_range_pkey
                        DO UPDATE
                        SET semester_part_name = %(SemesterPartName)s
                        ;
                    """, {
                        "SemesterPartName": names[i],
                        "DateStart": start_dates[i],
                        "DateEnd": end_dates[i]
                    }, isSELECT=False)
                    if (error):
                        return (False, error)
            return (True, None)
        return (False, None)
