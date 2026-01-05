class Vypujcka:
    """Vypujcka model"""
    
    def __init__(self, id=None, kniha_id=None, ctenar_id=None, 
                 datum_vypujceni=None, datum_vraceni=None, 
                 predpokladane_vraceni=None, stav='active', 
                 poznamka=None, created_at=None):
        self.id = id
        self.kniha_id = kniha_id
        self.ctenar_id = ctenar_id
        self.datum_vypujceni = datum_vypujceni
        self.datum_vraceni = datum_vraceni
        self.predpokladane_vraceni = predpokladane_vraceni
        self.stav = stav
        self.poznamka = poznamka
        self.created_at = created_at
        # Pro zobrazení
        self.kniha_nazev = None
        self.ctenar_jmeno = None
    
    def __str__(self):
        return f"Vypujcka #{self.id} - {self.stav}"
    
    def __repr__(self):
        return f"Vypujcka(id={self.id}, kniha_id={self.kniha_id}, ctenar_id={self.ctenar_id}, stav='{self.stav}')"
