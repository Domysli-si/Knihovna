class Zanr:
    """Zanr model"""
    
    def __init__(self, id=None, nazev=None, popis=None, created_at=None):
        self.id = id
        self.nazev = nazev
        self.popis = popis
        self.created_at = created_at
    
    def __str__(self):
        return self.nazev
    
    def __repr__(self):
        return f"Zanr(id={self.id}, nazev='{self.nazev}')"
