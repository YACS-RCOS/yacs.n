class semester_info:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def update(self, semester, isActive):
        self.db.execute("""
            UPDATE semester_info
            SET public=%s
            WHERE semester=%s
        """, [isActive, semester], isSELECT=False)