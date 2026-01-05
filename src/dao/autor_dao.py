from models.autor import Autor

class AutorDAO:
    """Data Access Object for Autor table"""
    
    def __init__(self, database):
        self.db = database
    
    def create(self, autor):
        """Insert new autor"""
        query = """
            INSERT INTO autori (jmeno, prijmeni, datum_narozeni, zeme_puvodu)
            VALUES (%s, %s, %s, %s)
        """
        params = (autor.jmeno, autor.prijmeni, autor.datum_narozeni, autor.zeme_puvodu)
        
        try:
            autor_id = self.db.execute_query(query, params)
            autor.id = autor_id
            return autor
        except Exception as e:
            raise Exception(f"Failed to create autor: {e}")
    
    def get_by_id(self, autor_id):
        """Get autor by ID"""
        query = "SELECT * FROM autori WHERE id = %s"
        
        try:
            results = self.db.execute_select(query, (autor_id,))
            if results:
                return self._map_to_object(results[0])
            return None
        except Exception as e:
            raise Exception(f"Failed to get autor: {e}")
    
    def get_all(self):
        """Get all autori"""
        query = "SELECT * FROM autori ORDER BY prijmeni, jmeno"
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get all autori: {e}")
    
    def update(self, autor):
        """Update autor"""
        query = """
            UPDATE autori 
            SET jmeno = %s, prijmeni = %s, datum_narozeni = %s, zeme_puvodu = %s
            WHERE id = %s
        """
        params = (autor.jmeno, autor.prijmeni, autor.datum_narozeni, 
                 autor.zeme_puvodu, autor.id)
        
        try:
            self.db.execute_query(query, params)
            return autor
        except Exception as e:
            raise Exception(f"Failed to update autor: {e}")
    
    def delete(self, autor_id):
        """Delete autor"""
        query = "DELETE FROM autori WHERE id = %s"
        
        try:
            self.db.execute_query(query, (autor_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to delete autor: {e}")
    
    def search_by_name(self, search_term):
        """Search autori by name"""
        query = """
            SELECT * FROM autori 
            WHERE jmeno LIKE %s OR prijmeni LIKE %s
            ORDER BY prijmeni, jmeno
        """
        search_pattern = f"%{search_term}%"
        
        try:
            results = self.db.execute_select(query, (search_pattern, search_pattern))
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to search autori: {e}")
    
    def _map_to_object(self, row):
        """Map database row to Autor object"""
        return Autor(
            id=row['id'],
            jmeno=row['jmeno'],
            prijmeni=row['prijmeni'],
            datum_narozeni=row['datum_narozeni'],
            zeme_puvodu=row['zeme_puvodu'],
            created_at=row['created_at']
        )
