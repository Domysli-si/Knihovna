class Kniha:
    """Kniha model"""
    
    def __init__(self, id=None, nazev=None, isbn=None, rok_vydani=None, 
                 pocet_stran=None, hodnoceni=None, dostupna=True, 
                 zanr_id=None, created_at=None):
        self.id = id
        self.nazev = nazev
        self.isbn = isbn
        self.rok_vydani = rok_vydani
        self.pocet_stran = pocet_stran
        self.hodnoceni = hodnoceni
        self.dostupna = dostupna
        self.zanr_id = zanr_id
        self.created_at = created_at
        # Pro zobrazení
        self.zanr_nazev = None
        self.autori = []
    
    def __str__(self):
        return f"{self.nazev} ({self.rok_vydani})"
    
    def __repr__(self):
        return f"Kniha(id={self.id}, nazev='{self.nazev}', isbn='{self.isbn}')"
