class Autor:
    """Autor model"""
    
    def __init__(self, id=None, jmeno=None, prijmeni=None, datum_narozeni=None, 
                 zeme_puvodu=None, created_at=None):
        self.id = id
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.datum_narozeni = datum_narozeni
        self.zeme_puvodu = zeme_puvodu
        self.created_at = created_at
    
    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"
    
    def __repr__(self):
        return f"Autor(id={self.id}, jmeno='{self.jmeno}', prijmeni='{self.prijmeni}')"
