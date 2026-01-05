from models.vypujcka import Vypujcka

class VypujckaDAO:
    """Data Access Object for Vypujcka table"""
    
    def __init__(self, database):
        self.db = database
    
    def create(self, vypujcka):
        """Insert new vypujcka"""
        query = """
            INSERT INTO vypujcky (kniha_id, ctenar_id, datum_vypujceni, 
                                 datum_vraceni, predpokladane_vraceni, stav, poznamka)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (vypujcka.kniha_id, vypujcka.ctenar_id, vypujcka.datum_vypujceni,
                 vypujcka.datum_vraceni, vypujcka.predpokladane_vraceni, 
                 vypujcka.stav, vypujcka.poznamka)
        
        try:
            vypujcka_id = self.db.execute_query(query, params)
            vypujcka.id = vypujcka_id
            return vypujcka
        except Exception as e:
            raise Exception(f"Failed to create vypujcka: {e}")
    
    def get_by_id(self, vypujcka_id):
        """Get vypujcka by ID with kniha and ctenar info"""
        query = """
            SELECT v.*, k.nazev as kniha_nazev, 
                   CONCAT(c.jmeno, ' ', c.prijmeni) as ctenar_jmeno
            FROM vypujcky v
            JOIN knihy k ON v.kniha_id = k.id
            JOIN ctenari c ON v.ctenar_id = c.id
            WHERE v.id = %s
        """
        
        try:
            results = self.db.execute_select(query, (vypujcka_id,))
            if results:
                return self._map_to_object(results[0])
            return None
        except Exception as e:
            raise Exception(f"Failed to get vypujcka: {e}")
    
    def get_all(self):
        """Get all vypujcky"""
        query = """
            SELECT v.*, k.nazev as kniha_nazev, 
                   CONCAT(c.jmeno, ' ', c.prijmeni) as ctenar_jmeno
            FROM vypujcky v
            JOIN knihy k ON v.kniha_id = k.id
            JOIN ctenari c ON v.ctenar_id = c.id
            ORDER BY v.datum_vypujceni DESC
        """
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get all vypujcky: {e}")
    
    def get_active(self):
        """Get active vypujcky"""
        query = """
            SELECT v.*, k.nazev as kniha_nazev, 
                   CONCAT(c.jmeno, ' ', c.prijmeni) as ctenar_jmeno
            FROM vypujcky v
            JOIN knihy k ON v.kniha_id = k.id
            JOIN ctenari c ON v.ctenar_id = c.id
            WHERE v.stav = 'active'
            ORDER BY v.predpokladane_vraceni
        """
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get active vypujcky: {e}")
    
    def get_by_ctenar(self, ctenar_id):
        """Get vypujcky by ctenar"""
        query = """
            SELECT v.*, k.nazev as kniha_nazev, 
                   CONCAT(c.jmeno, ' ', c.prijmeni) as ctenar_jmeno
            FROM vypujcky v
            JOIN knihy k ON v.kniha_id = k.id
            JOIN ctenari c ON v.ctenar_id = c.id
            WHERE v.ctenar_id = %s
            ORDER BY v.datum_vypujceni DESC
        """
        
        try:
            results = self.db.execute_select(query, (ctenar_id,))
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get vypujcky by ctenar: {e}")
    
    def get_by_kniha(self, kniha_id):
        """Get vypujcky by kniha"""
        query = """
            SELECT v.*, k.nazev as kniha_nazev, 
                   CONCAT(c.jmeno, ' ', c.prijmeni) as ctenar_jmeno
            FROM vypujcky v
            JOIN knihy k ON v.kniha_id = k.id
            JOIN ctenari c ON v.ctenar_id = c.id
            WHERE v.kniha_id = %s
            ORDER BY v.datum_vypujceni DESC
        """
        
        try:
            results = self.db.execute_select(query, (kniha_id,))
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get vypujcky by kniha: {e}")
    
    def update(self, vypujcka):
        """Update vypujcka"""
        query = """
            UPDATE vypujcky 
            SET kniha_id = %s, ctenar_id = %s, datum_vypujceni = %s,
                datum_vraceni = %s, predpokladane_vraceni = %s, stav = %s, poznamka = %s
            WHERE id = %s
        """
        params = (vypujcka.kniha_id, vypujcka.ctenar_id, vypujcka.datum_vypujceni,
                 vypujcka.datum_vraceni, vypujcka.predpokladane_vraceni,
                 vypujcka.stav, vypujcka.poznamka, vypujcka.id)
        
        try:
            self.db.execute_query(query, params)
            return vypujcka
        except Exception as e:
            raise Exception(f"Failed to update vypujcka: {e}")
    
    def return_book(self, vypujcka_id, datum_vraceni):
        """Mark vypujcka as returned"""
        query = """
            UPDATE vypujcky 
            SET datum_vraceni = %s, stav = 'returned'
            WHERE id = %s
        """
        
        try:
            self.db.execute_query(query, (datum_vraceni, vypujcka_id))
            return True
        except Exception as e:
            raise Exception(f"Failed to return book: {e}")
    
    def mark_overdue(self, vypujcka_id):
        """Mark vypujcka as overdue"""
        query = "UPDATE vypujcky SET stav = 'overdue' WHERE id = %s"
        
        try:
            self.db.execute_query(query, (vypujcka_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to mark overdue: {e}")

    def delete(self, vypujcka_id):
        """Cancel vypujcka (change state to cancelled)"""
        query = "UPDATE vypujcky SET stav = 'cancelled' WHERE id = %s"
        
        try:
            self.db.execute_query(query, (vypujcka_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to cancel vypujcka: {e}")
    
    def update_overdue_loans(self):
        """Update overdue loans automatically"""
        query = """
            UPDATE vypujcky 
            SET stav = 'overdue'
            WHERE stav = 'active' 
            AND predpokladane_vraceni < CURDATE()
        """
        
        try:
            self.db.execute_query(query)
            return True
        except Exception as e:
            raise Exception(f"Failed to update overdue loans: {e}")
    
    def get_overdue(self):
        """Get overdue vypujcky"""
        query = """
            SELECT v.*, k.nazev as kniha_nazev, 
                   CONCAT(c.jmeno, ' ', c.prijmeni) as ctenar_jmeno
            FROM vypujcky v
            JOIN knihy k ON v.kniha_id = k.id
            JOIN ctenari c ON v.ctenar_id = c.id
            WHERE v.stav = 'overdue'
            ORDER BY v.predpokladane_vraceni
        """
        
        try:
            results = self.db.execute_select(query)
            return [self._map_to_object(row) for row in results]
        except Exception as e:
            raise Exception(f"Failed to get overdue vypujcky: {e}")
    
    def _map_to_object(self, row):
        """Map database row to Vypujcka object"""
        vypujcka = Vypujcka(
            id=row['id'],
            kniha_id=row['kniha_id'],
            ctenar_id=row['ctenar_id'],
            datum_vypujceni=row['datum_vypujceni'],
            datum_vraceni=row['datum_vraceni'],
            predpokladane_vraceni=row['predpokladane_vraceni'],
            stav=row['stav'],
            poznamka=row['poznamka'],
            created_at=row['created_at']
        )
        vypujcka.kniha_nazev = row.get('kniha_nazev')
        vypujcka.ctenar_jmeno = row.get('ctenar_jmeno')
        return vypujcka
