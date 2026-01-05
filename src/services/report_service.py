import csv
from datetime import datetime

class ReportService:
    """Service for generating reports"""
    
    def __init__(self, database):
        self.db = database
    
    def generate_knihy_report(self, output_file='report_knihy.csv'):
        """Generate knihy report with aggregated data from multiple tables"""
        query = """
            SELECT 
                k.id,
                k.nazev,
                k.isbn,
                z.nazev as zanr,
                GROUP_CONCAT(CONCAT(a.jmeno, ' ', a.prijmeni) SEPARATOR ', ') as autori,
                k.rok_vydani,
                k.pocet_stran,
                k.hodnoceni,
                k.dostupna,
                COUNT(DISTINCT v.id) as pocet_vypujcek,
                COUNT(DISTINCT CASE WHEN v.stav = 'active' THEN v.id END) as aktivnich_vypujcek,
                COUNT(DISTINCT CASE WHEN v.stav = 'returned' THEN v.id END) as vraceno,
                COUNT(DISTINCT CASE WHEN v.stav = 'overdue' THEN v.id END) as po_terminu,
                MAX(v.datum_vypujceni) as posledni_vypujcka
            FROM knihy k
            LEFT JOIN zanry z ON k.zanr_id = z.id
            LEFT JOIN knihy_autori ka ON k.id = ka.kniha_id
            LEFT JOIN autori a ON ka.autor_id = a.id
            LEFT JOIN vypujcky v ON k.id = v.kniha_id
            GROUP BY k.id, k.nazev, k.isbn, z.nazev, k.rok_vydani, k.pocet_stran, k.hodnoceni, k.dostupna
            ORDER BY pocet_vypujcek DESC, k.nazev
        """
        
        try:
            results = self.db.execute_select(query)
            
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if not results:
                    f.write("No data available\n")
                    return output_file
                
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Failed to generate knihy report: {e}")
    
    def generate_vypujcky_report(self, output_file='report_vypujcky.csv'):
        """Generate vypujcky report with aggregated data from multiple tables"""
        query = """
            SELECT 
                v.id as vypujcka_id,
                k.nazev as kniha,
                k.isbn,
                CONCAT(c.jmeno, ' ', c.prijmeni) as ctenar,
                c.email as ctenar_email,
                v.datum_vypujceni,
                v.predpokladane_vraceni,
                v.datum_vraceni,
                v.stav,
                CASE 
                    WHEN v.stav = 'overdue' THEN DATEDIFF(CURDATE(), v.predpokladane_vraceni)
                    WHEN v.stav = 'returned' AND v.datum_vraceni > v.predpokladane_vraceni 
                        THEN DATEDIFF(v.datum_vraceni, v.predpokladane_vraceni)
                    ELSE 0
                END as dny_po_terminu,
                v.poznamka
            FROM vypujcky v
            JOIN knihy k ON v.kniha_id = k.id
            JOIN ctenari c ON v.ctenar_id = c.id
            WHERE v.stav != 'cancelled'
            ORDER BY v.datum_vypujceni DESC
        """
        
        try:
            results = self.db.execute_select(query)
            
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if not results:
                    f.write("No data available\n")
                    return output_file
                
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Failed to generate vypujcky report: {e}")
    
    def generate_ctenari_statistics(self, output_file='report_ctenari.csv'):
        """Generate ctenari statistics report"""
        query = """
            SELECT 
                c.id,
                CONCAT(c.jmeno, ' ', c.prijmeni) as jmeno,
                c.email,
                c.registrovan_od,
                c.aktivni,
                COUNT(DISTINCT v.id) as celkem_vypujcek,
                COUNT(DISTINCT CASE WHEN v.stav = 'active' THEN v.id END) as aktivnich_vypujcek,
                COUNT(DISTINCT CASE WHEN v.stav = 'overdue' THEN v.id END) as po_terminu,
                COUNT(DISTINCT CASE WHEN v.stav = 'returned' THEN v.id END) as vraceno,
                MAX(v.datum_vypujceni) as posledni_vypujcka
            FROM ctenari c
            LEFT JOIN vypujcky v ON c.id = v.ctenar_id
            GROUP BY c.id, c.jmeno, c.prijmeni, c.email, c.registrovan_od, c.aktivni
            ORDER BY celkem_vypujcek DESC
        """
        
        try:
            results = self.db.execute_select(query)
            
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if not results:
                    f.write("No data available\n")
                    return output_file
                
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Failed to generate ctenari statistics: {e}")
    
    def get_summary_statistics(self):
        """Get summary statistics from database"""
        queries = {
            'total_knihy': "SELECT COUNT(*) as count FROM knihy",
            'dostupne_knihy': "SELECT COUNT(*) as count FROM knihy WHERE dostupna = TRUE",
            'total_autori': "SELECT COUNT(*) as count FROM autori",
            'total_ctenari': "SELECT COUNT(*) as count FROM ctenari",
            'aktivni_ctenari': "SELECT COUNT(*) as count FROM ctenari WHERE aktivni = TRUE",
            'aktivni_vypujcky': "SELECT COUNT(*) as count FROM vypujcky WHERE stav = 'active'",
            'overdue_vypujcky': "SELECT COUNT(*) as count FROM vypujcky WHERE stav = 'overdue'",
            'total_vypujcky': "SELECT COUNT(*) as count FROM vypujcky WHERE stav != 'cancelled'"
        }
        
        statistics = {}
        
        try:
            for key, query in queries.items():
                result = self.db.execute_select(query)
                statistics[key] = result[0]['count'] if result else 0
            
            return statistics
            
        except Exception as e:
            raise Exception(f"Failed to get summary statistics: {e}")
