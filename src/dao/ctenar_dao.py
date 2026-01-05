from models.ctenar import Ctenar

class CtenarDAO:
    """Data Access Object for Ctenar table"""
    
    def __init__(self, database):
        self.db = database
    
    def create(self, ctenar):
        """Insert new ctenar"""
        query = """
            INSERT INTO ctenari (jmeno, prijmeni, email, telefon, registrovan_od, aktivni)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (ctenar.jmeno, ctenar.prijmeni, ctenar.email, ctenar.telefon,
                 ctenar.registrovan_od, ctenar.aktivni)
        
        try:
            ctenar_id = self.db.execute_query(query, params)
            ctenar.id = ctenar_id
            return ctenar
        except Exception as e:
            raise Exception(f"Failed to create ctenar: {e}")
    
    def get_by_id(self, ctenar_id):
        """Get ctenar by ID"""
        query = "SELECT * FROM ctenari WHERE id = %s"
        
        try:
            results = self.db.execute_select(query, (ctenar_id,))
            if results:
                return self._map_to_object(results[0])
            return None
        except Exception as e:
            raise Exception(f"Failed to get ctenar: {e}")
    
    def get_all(self):
        """Get all ctenari"""
        query = "SELECT * FROM ctenari ORDER BY prijmeni, jmeno"
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get all ctenari: {e}")
    
    def get_active(self):
        """Get active ctenari"""
        query = "SELECT * FROM ctenari WHERE aktivni = TRUE ORDER BY prijmeni, jmeno"
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get active ctenari: {e}")
    
    def update(self, ctenar):
        """Update ctenar"""
        query = """
            UPDATE ctenari 
            SET jmeno = %s, prijmeni = %s, email = %s, telefon = %s,
                registrovan_od = %s, aktivni = %s
            WHERE id = %s
        """
        params = (ctenar.jmeno, ctenar.prijmeni, ctenar.email, ctenar.telefon,
                 ctenar.registrovan_od, ctenar.aktivni, ctenar.id)
        
        try:
            self.db.execute_query(query, params)
            return ctenar
        except Exception as e:
            raise Exception(f"Failed to update ctenar: {e}")
    
    def delete(self, ctenar_id):
        """Delete ctenar"""
        query = "DELETE FROM ctenari WHERE id = %s"
        
        try:
            self.db.execute_query(query, (ctenar_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to delete ctenar: {e}")
    
    def search_by_name(self, search_term):
        """Search ctenari by name"""
        query = """
            SELECT * FROM ctenari 
            WHERE jmeno LIKE %s OR prijmeni LIKE %s
            ORDER BY prijmeni, jmeno
        """
        search_pattern = f"%{search_term}%"
        
        try:
            results = self.db.execute_select(query, (search_pattern, search_pattern))
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to search ctenari: {e}")
    
    def search_by_email(self, email):
        """Search ctenar by email"""
        query = "SELECT * FROM ctenari WHERE email = %s"
        
        try:
            results = self.db.execute_select(query, (email,))
            if results:
                return self._map_to_object(results[0])
            return None
        except Exception as e:
            raise Exception(f"Failed to search by email: {e}")
    
    def _map_to_object(self, row):
        """Map database row to Ctenar object"""
        return Ctenar(
            id=row['id'],
            jmeno=row['jmeno'],
            prijmeni=row['prijmeni'],
            email=row['email'],
            telefon=row['telefon'],
            registrovan_od=row['registrovan_od'],
            aktivni=bool(row['aktivni']),
            created_at=row['created_at']
        )
