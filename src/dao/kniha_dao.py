from models.kniha import Kniha

class KnihaDAO:
    """Data Access Object for Kniha table"""
    
    def __init__(self, database):
        self.db = database
    
    def create(self, kniha):
        """Insert new kniha"""
        query = """
            INSERT INTO knihy (nazev, isbn, rok_vydani, pocet_stran, hodnoceni, dostupna, zanr_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (kniha.nazev, kniha.isbn, kniha.rok_vydani, kniha.pocet_stran,
                 kniha.hodnoceni, kniha.dostupna, kniha.zanr_id)
        
        try:
            kniha_id = self.db.execute_query(query, params)
            kniha.id = kniha_id
            return kniha
        except Exception as e:
            raise Exception(f"Failed to create kniha: {e}")
    
    def get_by_id(self, kniha_id):
        """Get kniha by ID with zanr info"""
        query = """
            SELECT k.*, z.nazev as zanr_nazev
            FROM knihy k
            LEFT JOIN zanry z ON k.zanr_id = z.id
            WHERE k.id = %s
        """
        
        try:
            results = self.db.execute_select(query, (kniha_id,))
            if results:
                return self._map_to_object(results[0])
            return None
        except Exception as e:
            raise Exception(f"Failed to get kniha: {e}")
    
    def get_all(self):
        """Get all knihy with zanr info"""
        query = """
            SELECT k.*, z.nazev as zanr_nazev
            FROM knihy k
            LEFT JOIN zanry z ON k.zanr_id = z.id
            ORDER BY k.nazev
        """
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get all knihy: {e}")
    
    def get_available(self):
        """Get available knihy"""
        query = """
            SELECT k.*, z.nazev as zanr_nazev
            FROM knihy k
            LEFT JOIN zanry z ON k.zanr_id = z.id
            WHERE k.dostupna = TRUE
            ORDER BY k.nazev
        """
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get available knihy: {e}")
    
    def update(self, kniha):
        """Update kniha"""
        query = """
            UPDATE knihy 
            SET nazev = %s, isbn = %s, rok_vydani = %s, pocet_stran = %s,
                hodnoceni = %s, dostupna = %s, zanr_id = %s
            WHERE id = %s
        """
        params = (kniha.nazev, kniha.isbn, kniha.rok_vydani, kniha.pocet_stran,
                 kniha.hodnoceni, kniha.dostupna, kniha.zanr_id, kniha.id)
        
        try:
            self.db.execute_query(query, params)
            return kniha
        except Exception as e:
            raise Exception(f"Failed to update kniha: {e}")
    
    def delete(self, kniha_id):
        """Delete kniha"""
        query = "DELETE FROM knihy WHERE id = %s"
        
        try:
            self.db.execute_query(query, (kniha_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to delete kniha: {e}")
    
    def set_availability(self, kniha_id, dostupna):
        """Set kniha availability"""
        query = "UPDATE knihy SET dostupna = %s WHERE id = %s"
        
        try:
            self.db.execute_query(query, (dostupna, kniha_id))
            return True
        except Exception as e:
            raise Exception(f"Failed to set availability: {e}")
    
    def search_by_title(self, search_term):
        """Search knihy by title"""
        query = """
            SELECT k.*, z.nazev as zanr_nazev
            FROM knihy k
            LEFT JOIN zanry z ON k.zanr_id = z.id
            WHERE k.nazev LIKE %s
            ORDER BY k.nazev
        """
        search_pattern = f"%{search_term}%"
        
        try:
            results = self.db.execute_select(query, (search_pattern,))
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to search knihy: {e}")
    
    def add_autor(self, kniha_id, autor_id, poradi=1):
        """Link kniha with autor (M:N)"""
        query = "INSERT INTO knihy_autori (kniha_id, autor_id, poradi) VALUES (%s, %s, %s)"
        
        try:
            self.db.execute_query(query, (kniha_id, autor_id, poradi))
            return True
        except Exception as e:
            raise Exception(f"Failed to add autor to kniha: {e}")
    
    def remove_autor(self, kniha_id, autor_id):
        """Unlink kniha from autor"""
        query = "DELETE FROM knihy_autori WHERE kniha_id = %s AND autor_id = %s"
        
        try:
            self.db.execute_query(query, (kniha_id, autor_id))
            return True
        except Exception as e:
            raise Exception(f"Failed to remove autor from kniha: {e}")
    
    def get_autori(self, kniha_id):
        """Get all autori for kniha"""
        query = """
            SELECT a.* FROM autori a
            JOIN knihy_autori ka ON a.id = ka.autor_id
            WHERE ka.kniha_id = %s
            ORDER BY ka.poradi
        """
        
        try:
            from models.autor import Autor
            results = self.db.execute_select(query, (kniha_id,))
            return [Autor(
                id=row['id'],
                jmeno=row['jmeno'],
                prijmeni=row['prijmeni'],
                datum_narozeni=row['datum_narozeni'],
                zeme_puvodu=row['zeme_puvodu'],
                created_at=row['created_at']
            ) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get kniha autori: {e}")
    
    def _map_to_object(self, row):
        """Map database row to Kniha object"""
        kniha = Kniha(
            id=row['id'],
            nazev=row['nazev'],
            isbn=row['isbn'],
            rok_vydani=row['rok_vydani'],
            pocet_stran=row['pocet_stran'],
            hodnoceni=row['hodnoceni'],
            dostupna=bool(row['dostupna']),
            zanr_id=row['zanr_id'],
            created_at=row['created_at']
        )
        kniha.zanr_nazev = row.get('zanr_nazev')
        return kniha
