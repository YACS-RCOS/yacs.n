import string


class Majors:
    
    def __init__(self, db_wrapper):
        self.db = db_wrapper
    
    def reset_majors(self):
        self.db.execute("""
            DELETE FROM major_list
        """, {
        
        }, isSELECT=False);
    
    def upsert(self, major, degree_types):
        degree_types = degree_types.upper()
        # degreeType should be a string consisting of B if it offered for Bachelors, M if offered for masters, and D if offered as a PhD. For example,
        # if a degree is offered for all three types, degreeTypes should be "BMD"
        self.db.execute("""
            INSERT INTO major_list(major, b, m ,d)
            VALUES (%(Major)s, %(isB)s, %(isM)s, %(isD)s)
            ;
        """,
        {
            "Major": major,
            "isB": ('B' in degree_types),
            "isM": ('M' in degree_types),
            "isD": ('D' in degree_types),
        }, isSELECT=False)
    
    def list_majors_in_degreetype(self, degreetype):
        assert len(degreetype) == 1
        if not degreetype.upper() in ["B", "M", "D"]:
            return None, f"Unknown major type {degreetype}"
            
        sql = f"""
            SELECT major
            FROM major_list
            WHERE {degreetype.lower()};
        """
        data, error = self.db.execute(sql, {}, isSELECT=True)
        
        return (data, None) if not error else (None, error)