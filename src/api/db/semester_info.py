class semester_info:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def upsert(self, semester, isPublic):
        self.db.execute("""
            INSERT INTO semester_info (semester, public)
            VALUES (%(SemesterName)s, %(IsPublic)s)
            ON CONFLICT ON CONSTRAINT semester_info_pkey
            DO UPDATE
            SET public=%(IsPublic)s
            ;
        """,
        {
            "SemesterName": semester,
            "IsPublic": isPublic
        }, isSELECT=False)