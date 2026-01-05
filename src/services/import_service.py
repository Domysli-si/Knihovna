import csv
import os
from datetime import datetime
from models.autor import Autor
from models.kniha import Kniha

class ImportService:
    """Service for importing data from CSV files"""
    
    def __init__(self, database, autor_dao, kniha_dao, zanr_dao):
        self.db = database
        self.autor_dao = autor_dao
        self.kniha_dao = kniha_dao
        self.zanr_dao = zanr_dao
    
    def import_autori_from_csv(self, csv_file):
        """Import autori from CSV file"""
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        imported_count = 0
        errors = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate required fields
                        if not row.get('jmeno') or not row.get('prijmeni'):
                            errors.append(f"Row {row_num}: Missing required fields (jmeno, prijmeni)")
                            continue
                        
                        # Parse datum_narozeni
                        datum_narozeni = None
                        if row.get('datum_narozeni'):
                            try:
                                datum_narozeni = datetime.strptime(row['datum_narozeni'], '%Y-%m-%d').date()
                            except ValueError:
                                errors.append(f"Row {row_num}: Invalid date format for datum_narozeni (use YYYY-MM-DD)")
                                continue
                        
                        # Create Autor object
                        autor = Autor(
                            jmeno=row['jmeno'].strip(),
                            prijmeni=row['prijmeni'].strip(),
                            datum_narozeni=datum_narozeni,
                            zeme_puvodu=row.get('zeme_puvodu', '').strip() or None
                        )
                        
                        # Save to database
                        self.autor_dao.create(autor)
                        imported_count += 1
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
            
            return {
                'success': True,
                'imported': imported_count,
                'errors': errors
            }
            
        except Exception as e:
            raise Exception(f"Failed to import autori: {e}")
    
    def import_knihy_from_csv(self, csv_file):
        """Import knihy from CSV file"""
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        imported_count = 0
        errors = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate required fields
                        if not row.get('nazev'):
                            errors.append(f"Row {row_num}: Missing required field (nazev)")
                            continue
                        
                        # Parse numeric fields
                        rok_vydani = int(row['rok_vydani']) if row.get('rok_vydani') else None
                        pocet_stran = int(row['pocet_stran']) if row.get('pocet_stran') else None
                        hodnoceni = float(row['hodnoceni']) if row.get('hodnoceni') else 0.0
                        
                        # Validate hodnoceni range
                        if hodnoceni < 0.0 or hodnoceni > 5.0:
                            errors.append(f"Row {row_num}: Hodnoceni must be between 0.0 and 5.0")
                            continue
                        
                        # Find zanr by name
                        zanr_id = None
                        if row.get('zanr_nazev'):
                            zanry = self.zanr_dao.get_all()
                            for zanr in zanry:
                                if zanr.nazev.lower() == row['zanr_nazev'].strip().lower():
                                    zanr_id = zanr.id
                                    break
                            
                            if not zanr_id:
                                errors.append(f"Row {row_num}: Zanr '{row['zanr_nazev']}' not found")
                                continue
                        
                        # Parse dostupna
                        dostupna = True
                        if row.get('dostupna'):
                            dostupna = row['dostupna'].strip().lower() in ('true', '1', 'ano', 'yes')
                        
                        # Create Kniha object
                        kniha = Kniha(
                            nazev=row['nazev'].strip(),
                            isbn=row.get('isbn', '').strip() or None,
                            rok_vydani=rok_vydani,
                            pocet_stran=pocet_stran,
                            hodnoceni=hodnoceni,
                            dostupna=dostupna,
                            zanr_id=zanr_id
                        )
                        
                        # Save to database
                        self.kniha_dao.create(kniha)
                        
                        # Link with autor if specified
                        if row.get('autor_prijmeni'):
                            autori = self.autor_dao.search_by_name(row['autor_prijmeni'].strip())
                            if autori:
                                self.kniha_dao.add_autor(kniha.id, autori[0].id)
                            else:
                                errors.append(f"Row {row_num}: Autor '{row['autor_prijmeni']}' not found, kniha created without autor")
                        
                        imported_count += 1
                        
                    except ValueError as e:
                        errors.append(f"Row {row_num}: Invalid number format - {str(e)}")
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
            
            return {
                'success': True,
                'imported': imported_count,
                'errors': errors
            }
            
        except Exception as e:
            raise Exception(f"Failed to import knihy: {e}")
    
    def validate_csv_format(self, csv_file, required_columns):
        """Validate CSV file format"""
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                missing_columns = [col for col in required_columns if col not in headers]
                
                if missing_columns:
                    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
                
                return True
                
        except Exception as e:
            raise Exception(f"CSV validation failed: {e}")
