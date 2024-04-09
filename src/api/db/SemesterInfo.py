import asyncio

class SemesterInfo:
    def __init__(self, db_wrapper, cache):
        self.db = db_wrapper
        self.cache = cache

    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))

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

    def is_public(self, semester):
        """
        @param: semester name
        @returns: Boolean indicating if the semester is publicly viewable
        """
        data, error = self.db.execute("""
            SELECT public FROM semester_info WHERE semester=%s LIMIT 1;
        """, [semester], isSELECT=True)
        if data is not None and len(data) > 0:
            return data[0]['public']
        return False

    def delete_semester(self, semester):
        # clear cache so this semester does not come up again
        self.clear_cache()
        return self.db.execute("""
            BEGIN TRANSACTION;
                DELETE FROM semester_info
                WHERE semester=%(Semester)s;
            COMMIT;
        """, {
            "Semester": semester
        }, isSELECT=False)