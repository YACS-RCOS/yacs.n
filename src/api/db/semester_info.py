from db.model import *

class semester_info(Model):

    def __init__(self):
        super().__init__()

    async def upsert(self, semester, isPublic):
        await self.db.execute("""
            INSERT INTO semester_info (semester, public)
            VALUES ('%(SemesterName)s', '%(IsPublic)s')
            ON CONFLICT ON CONSTRAINT semester_info_pkey
            DO UPDATE
            SET public='%(IsPublic)s'
            ;
        """,
        {
            "SemesterName": semester,
            "IsPublic": isPublic
        }, isSELECT=False)

    async def is_public(self, semester):
        """
        @param: semester name
        @returns: Boolean indicating if the semester is publicly viewable
        """
        data, error = await self.db.execute("""
            SELECT public FROM semester_info WHERE semester='%s' LIMIT 1;
        """, (semester), isSELECT=True)
        if data is not None and len(data) > 0:
            return data[0]['public']
        return False
