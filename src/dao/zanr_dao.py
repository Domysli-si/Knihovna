from models.zanr import Zanr

class ZanrDAO:
    """Data Access Object for Zanr table"""
    
    def __init__(self, database):
        self.db = database
    
    def create(self, zanr):
        """Insert new zanr"""
        query = "INSERT INTO zanry (nazev, popis) VALUES (%s, %s)"
        params = (zanr.nazev, zanr.popis)
        
        try:
            zanr_id = self.db.execute_query(query, params)
            zanr.id = zanr_id
            return zanr
        except Exception as e:
            raise Exception(f"Failed to create zanr: {e}")
    
    def get_by_id(self, zanr_id):
        """Get zanr by ID"""
        query = "SELECT * FROM zanry WHERE id = %s"
        
        try:
            results = self.db.execute_select(query, (zanr_id,))
            if results:
                return self._map_to_object(results[0])
            return None
        except Exception as e:
            raise Exception(f"Failed to get zanr: {e}")
    
    def get_all(self):
        """Get all zanry"""
        query = "SELECT * FROM zanry ORDER BY nazev"
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get all zanry: {e}")
    
    def update(self, zanr):
        """Update zanr"""
        query = "UPDATE zanry SET nazev = %s, popis = %s WHERE id = %s"
        params = (zanr.nazev, zanr.popis, zanr.id)
        
        try:
            self.db.execute_query(query, params)
            return zanr
        except Exception as e:
            raise Exception(f"Failed to update zanr: {e}")
    
    def delete(self, zanr_id):
        """Delete zanr"""
        query = "DELETE FROM zanry WHERE id = %s"
        
        try:
            self.db.execute_query(query, (zanr_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to delete zanr: {e}")
    
    def _map_to_object(self, row):
        """Map database row to Zanr object"""
        return Zanr(
            id=row['id'],
            nazev=row['nazev'],
            popis=row['popis'],
            created_at=row['created_at']
        )
