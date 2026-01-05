from datetime import datetime

class TransactionService:
    """Service for handling database transactions"""
    
    def __init__(self, database, kniha_dao, vypujcka_dao):
        self.db = database
        self.kniha_dao = kniha_dao
        self.vypujcka_dao = vypujcka_dao
    
    def create_vypujcka_transaction(self, kniha_id, ctenar_id, predpokladane_vraceni, poznamka=None):
        """
        Create new vypujcka with transaction:
        1. Insert vypujcka record
        2. Set kniha.dostupna = FALSE
        Both operations must succeed or both fail
        """
        queries = [
            # Insert vypujcka
            ("""
                INSERT INTO vypujcky (kniha_id, ctenar_id, datum_vypujceni, 
                                     predpokladane_vraceni, stav, poznamka)
                VALUES (%s, %s, %s, %s, 'active', %s)
            """, (kniha_id, ctenar_id, datetime.now(), predpokladane_vraceni, poznamka)),
            
            # Update kniha availability
            ("UPDATE knihy SET dostupna = FALSE WHERE id = %s", (kniha_id,))
        ]
        
        try:
            results = self.db.execute_transaction(queries)
            vypujcka_id = results[0]  # First query returns inserted ID
            return vypujcka_id
        except Exception as e:
            raise Exception(f"Transaction failed: {e}")
    
    def return_book_transaction(self, vypujcka_id, kniha_id):
        """
        Return book with transaction:
        1. Update vypujcka (set returned, set datum_vraceni)
        2. Set kniha.dostupna = TRUE
        Both operations must succeed or both fail
        """
        queries = [
            # Update vypujcka
            ("""
                UPDATE vypujcky 
                SET stav = 'returned', datum_vraceni = %s
                WHERE id = %s
            """, (datetime.now(), vypujcka_id)),
            
            # Update kniha availability
            ("UPDATE knihy SET dostupna = TRUE WHERE id = %s", (kniha_id,))
        ]
        
        try:
            self.db.execute_transaction(queries)
            return True
        except Exception as e:
            raise Exception(f"Transaction failed: {e}")
    
    def cancel_vypujcka_transaction(self, vypujcka_id, kniha_id):
        """
        Cancel vypujcka with transaction:
        1. Update vypujcka state to cancelled
        2. Set kniha.dostupna = TRUE
        Both operations must succeed or both fail
        """
        queries = [
            # Cancel vypujcka
            ("UPDATE vypujcky SET stav = 'cancelled' WHERE id = %s", (vypujcka_id,)),
            
            # Update kniha availability
            ("UPDATE knihy SET dostupna = TRUE WHERE id = %s", (kniha_id,))
        ]
        
        try:
            self.db.execute_transaction(queries)
            return True
        except Exception as e:
            raise Exception(f"Transaction failed: {e}")
