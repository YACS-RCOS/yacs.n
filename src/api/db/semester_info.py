class SemesterInfo:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def upsert(self, semester, is_public):
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
            "IsPublic": is_public
        }, is_select=False)

    def is_public(self, semester):
        """
        @param: semester name
        @returns: Boolean indicating if the semester is publicly viewable
        """
        data, _error = self.db.execute("""
            SELECT public FROM semester_info WHERE semester=%s LIMIT 1;
        """, [semester], is_select=True)
        if data is not None and len(data) > 0:
            return data[0]['public']
        return False
