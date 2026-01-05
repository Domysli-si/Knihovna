class Ctenar:
    """Ctenar model"""
    
    def __init__(self, id=None, jmeno=None, prijmeni=None, email=None, 
                 telefon=None, registrovan_od=None, aktivni=True, created_at=None):
        self.id = id
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.email = email
        self.telefon = telefon
        self.registrovan_od = registrovan_od
        self.aktivni = aktivni
        self.created_at = created_at
    
    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"
    
    def __repr__(self):
        return f"Ctenar(id={self.id}, jmeno='{self.jmeno}', prijmeni='{self.prijmeni}', email='{self.email}')"
