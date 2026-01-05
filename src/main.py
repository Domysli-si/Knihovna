import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from database import Database
from dao import AutorDAO, ZanrDAO, KnihaDAO, CtenarDAO, VypujckaDAO
from models import Autor, Zanr, Kniha, Ctenar, Vypujcka
from services import ImportService, ReportService, TransactionService


class LibraryApp:
    """Main Library Management Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Knihovna - Správa knihovního systému")
        self.root.geometry("1200x700")
        
        # Initialize configuration and database
        try:
            self.config = Config()
            db_config = self.config.get_database_config()
            self.db = Database(db_config)
        except Exception as e:
            messagebox.showerror("Chyba konfigurace", str(e))
            sys.exit(1)
        
        # Initialize DAOs
        self.autor_dao = AutorDAO(self.db)
        self.zanr_dao = ZanrDAO(self.db)
        self.kniha_dao = KnihaDAO(self.db)
        self.ctenar_dao = CtenarDAO(self.db)
        self.vypujcka_dao = VypujckaDAO(self.db)
        
        # Initialize Services
        self.import_service = ImportService(self.db, self.autor_dao, self.kniha_dao, self.zanr_dao)
        self.report_service = ReportService(self.db)
        self.transaction_service = TransactionService(self.db, self.kniha_dao, self.vypujcka_dao)
        
        # Create UI
        self.create_menu()
        self.create_main_frame()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Autoři menu
        autori_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Autoři", menu=autori_menu)
        autori_menu.add_command(label="Zobrazit autory", command=self.show_autori)
        autori_menu.add_command(label="Přidat autora", command=self.add_autor)
        
        # Žánry menu
        zanry_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Žánry", menu=zanry_menu)
        zanry_menu.add_command(label="Zobrazit žánry", command=self.show_zanry)
        zanry_menu.add_command(label="Přidat žánr", command=self.add_zanr)
        
        # Knihy menu
        knihy_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Knihy", menu=knihy_menu)
        knihy_menu.add_command(label="Zobrazit knihy", command=self.show_knihy)
        knihy_menu.add_command(label="Přidat knihu", command=self.add_kniha)
        
        # Čtenáři menu
        ctenari_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Čtenáři", menu=ctenari_menu)
        ctenari_menu.add_command(label="Zobrazit čtenáře", command=self.show_ctenari)
        ctenari_menu.add_command(label="Přidat čtenáře", command=self.add_ctenar)
        
        # Výpůjčky menu
        vypujcky_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Výpůjčky", menu=vypujcky_menu)
        vypujcky_menu.add_command(label="Zobrazit výpůjčky", command=self.show_vypujcky)
        vypujcky_menu.add_command(label="Nová výpůjčka", command=self.add_vypujcka)
        vypujcky_menu.add_separator()
        vypujcky_menu.add_command(label="Aktualizovat po termínu", command=self.update_overdue)
        
        # Import menu
        import_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Import", menu=import_menu)
        import_menu.add_command(label="Importovat autory (CSV)", command=self.import_autori)
        import_menu.add_command(label="Importovat knihy (CSV)", command=self.import_knihy)
        
        # Reporty menu
        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reporty", menu=report_menu)
        report_menu.add_command(label="Report knih", command=self.generate_knihy_report)
        report_menu.add_command(label="Report výpůjček", command=self.generate_vypujcky_report)
        report_menu.add_command(label="Statistiky čtenářů", command=self.generate_ctenari_report)
        report_menu.add_separator()
        report_menu.add_command(label="Souhrnné statistiky", command=self.show_statistics)
    
    def create_main_frame(self):
        """Create main content frame"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def clear_main_frame(self):
        """Clear main frame content"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_welcome(self):
        """Show welcome screen"""
        self.clear_main_frame()
        
        welcome_label = ttk.Label(
            self.main_frame,
            text="Vítejte v knihovním systému",
            font=("Arial", 24, "bold")
        )
        welcome_label.pack(pady=50)
        
        info_label = ttk.Label(
            self.main_frame,
            text="Vyberte akci z menu výše",
            font=("Arial", 14)
        )
        info_label.pack(pady=20)
        
        # Show summary statistics
        try:
            stats = self.report_service.get_summary_statistics()
            stats_frame = ttk.LabelFrame(self.main_frame, text="Přehled", padding=20)
            stats_frame.pack(pady=20)
            
            ttk.Label(stats_frame, text=f"Celkem knih: {stats['total_knihy']}", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
            ttk.Label(stats_frame, text=f"Dostupných knih: {stats['dostupne_knihy']}", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
            ttk.Label(stats_frame, text=f"Celkem autorů: {stats['total_autori']}", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
            ttk.Label(stats_frame, text=f"Celkem čtenářů: {stats['total_ctenari']}", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
            ttk.Label(stats_frame, text=f"Aktivních výpůjček: {stats['aktivni_vypujcky']}", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
            ttk.Label(stats_frame, text=f"Po termínu: {stats['overdue_vypujcky']}", font=("Arial", 12), foreground="red").grid(row=5, column=0, sticky="w", pady=5)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst statistiky: {e}")
    
    # ==================== AUTOŘI ====================
    
    def show_autori(self):
        """Show authors list"""
        self.clear_main_frame()
        
        ttk.Label(self.main_frame, text="Seznam autorů", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Přidat autora", command=self.add_autor).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Obnovit", command=self.show_autori).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(pady=10)
        
        ttk.Label(search_frame, text="Hledat:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search_autori():
            term = search_var.get()
            if term:
                try:
                    autori = self.autor_dao.search_by_name(term)
                    self.populate_autori_tree(tree, autori)
                except Exception as e:
                    messagebox.showerror("Chyba", str(e))
            else:
                self.show_autori()
        
        ttk.Button(search_frame, text="Hledat", command=search_autori).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Jméno", "Příjmení", "Datum narození", "Země")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load data
        try:
            autori = self.autor_dao.get_all()
            self.populate_autori_tree(tree, autori)
        except Exception as e:
            messagebox.showerror("Chyba", str(e))
        
        # Context menu
        def on_right_click(event):
            item = tree.selection()
            if item:
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="Upravit", command=lambda: self.edit_autor(tree))
                menu.add_command(label="Smazat", command=lambda: self.delete_autor(tree))
                menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", on_right_click)
        tree.bind("<Double-1>", lambda e: self.edit_autor(tree))
    
    def populate_autori_tree(self, tree, autori):
        """Populate authors treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        for autor in autori:
            tree.insert("", tk.END, values=(
                autor.id,
                autor.jmeno,
                autor.prijmeni,
                autor.datum_narozeni or "",
                autor.zeme_puvodu or ""
            ))
    
    def add_autor(self):
        """Add new author dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Přidat autora")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Jméno:*").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        jmeno_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=jmeno_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Příjmení:*").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        prijmeni_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=prijmeni_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Datum narození:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(dialog, text="(YYYY-MM-DD)", font=("Arial", 8)).grid(row=2, column=1, sticky="w", padx=10)
        datum_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=datum_var, width=30).grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Země původu:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        zeme_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=zeme_var, width=30).grid(row=4, column=1, padx=10, pady=5)
        
        def save():
            jmeno = jmeno_var.get().strip()
            prijmeni = prijmeni_var.get().strip()
            
            if not jmeno or not prijmeni:
                messagebox.showwarning("Upozornění", "Vyplňte povinná pole (jméno, příjmení)")
                return
            
            datum_narozeni = None
            if datum_var.get().strip():
                try:
                    datum_narozeni = datetime.strptime(datum_var.get().strip(), "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("Chyba", "Neplatný formát data (použijte YYYY-MM-DD)")
                    return
            
            autor = Autor(
                jmeno=jmeno,
                prijmeni=prijmeni,
                datum_narozeni=datum_narozeni,
                zeme_puvodu=zeme_var.get().strip() or None
            )
            
            try:
                self.autor_dao.create(autor)
                messagebox.showinfo("Úspěch", "Autor byl přidán")
                dialog.destroy()
                self.show_autori()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Uložit", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Zrušit", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_autor(self, tree):
        """Edit author dialog"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Upozornění", "Vyberte autora ke úpravě")
            return
        
        item = tree.item(selection[0])
        autor_id = item['values'][0]
        
        try:
            autor = self.autor_dao.get_by_id(autor_id)
            if not autor:
                messagebox.showerror("Chyba", "Autor nenalezen")
                return
        except Exception as e:
            messagebox.showerror("Chyba", str(e))
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Upravit autora")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields (prepopulated)
        ttk.Label(dialog, text="Jméno:*").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        jmeno_var = tk.StringVar(value=autor.jmeno)
        ttk.Entry(dialog, textvariable=jmeno_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Příjmení:*").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        prijmeni_var = tk.StringVar(value=autor.prijmeni)
        ttk.Entry(dialog, textvariable=prijmeni_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Datum narození:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(dialog, text="(YYYY-MM-DD)", font=("Arial", 8)).grid(row=2, column=1, sticky="w", padx=10)
        datum_var = tk.StringVar(value=autor.datum_narozeni.strftime("%Y-%m-%d") if autor.datum_narozeni else "")
        ttk.Entry(dialog, textvariable=datum_var, width=30).grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Země původu:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        zeme_var = tk.StringVar(value=autor.zeme_puvodu or "")
        ttk.Entry(dialog, textvariable=zeme_var, width=30).grid(row=4, column=1, padx=10, pady=5)
        
        def save():
            jmeno = jmeno_var.get().strip()
            prijmeni = prijmeni_var.get().strip()
            
            if not jmeno or not prijmeni:
                messagebox.showwarning("Upozornění", "Vyplňte povinná pole")
                return
            
            datum_narozeni = None
            if datum_var.get().strip():
                try:
                    datum_narozeni = datetime.strptime(datum_var.get().strip(), "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("Chyba", "Neplatný formát data")
                    return
            
            autor.jmeno = jmeno
            autor.prijmeni = prijmeni
            autor.datum_narozeni = datum_narozeni
            autor.zeme_puvodu = zeme_var.get().strip() or None
            
            try:
                self.autor_dao.update(autor)
                messagebox.showinfo("Úspěch", "Autor byl upraven")
                dialog.destroy()
                self.show_autori()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Uložit", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Zrušit", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_autor(self, tree):
        """Delete author"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Upozornění", "Vyberte autora ke smazání")
            return
        
        item = tree.item(selection[0])
        autor_id = item['values'][0]
        autor_name = f"{item['values'][1]} {item['values'][2]}"
        
        if messagebox.askyesno("Potvrzení", f"Opravdu smazat autora {autor_name}?"):
            try:
                self.autor_dao.delete(autor_id)
                messagebox.showinfo("Úspěch", "Autor byl smazán")
                self.show_autori()
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se smazat autora: {e}")
    
    # ==================== ŽÁNRY ====================
    
    def show_zanry(self):
        """Show genres list"""
        self.clear_main_frame()
        
        ttk.Label(self.main_frame, text="Seznam žánrů", font=("Arial", 16, "bold")).pack(pady=10)
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Přidat žánr", command=self.add_zanr).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Obnovit", command=self.show_zanry).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Název", "Popis")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Název", text="Název")
        tree.heading("Popis", text="Popis")
        
        tree.column("ID", width=50)
        tree.column("Název", width=200)
        tree.column("Popis", width=400)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        try:
            zanry = self.zanr_dao.get_all()
            for zanr in zanry:
                tree.insert("", tk.END, values=(
                    zanr.id,
                    zanr.nazev,
                    zanr.popis or ""
                ))
        except Exception as e:
            messagebox.showerror("Chyba", str(e))
        
        def on_right_click(event):
            item = tree.selection()
            if item:
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="Upravit", command=lambda: self.edit_zanr(tree))
                menu.add_command(label="Smazat", command=lambda: self.delete_zanr(tree))
                menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", on_right_click)
        tree.bind("<Double-1>", lambda e: self.edit_zanr(tree))
    
    def add_zanr(self):
        """Add new genre dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Přidat žánr")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Název:*").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nazev_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=nazev_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Popis:").grid(row=1, column=0, sticky="nw", padx=10, pady=5)
        popis_text = tk.Text(dialog, width=30, height=5)
        popis_text.grid(row=1, column=1, padx=10, pady=5)
        
        def save():
            nazev = nazev_var.get().strip()
            if not nazev:
                messagebox.showwarning("Upozornění", "Vyplňte název žánru")
                return
            
            zanr = Zanr(
                nazev=nazev,
                popis=popis_text.get("1.0", tk.END).strip() or None
            )
            
            try:
                self.zanr_dao.create(zanr)
                messagebox.showinfo("Úspěch", "Žánr byl přidán")
                dialog.destroy()
                self.show_zanry()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Uložit", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Zrušit", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_zanr(self, tree):
        """Edit genre dialog"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Upozornění", "Vyberte žánr k úpravě")
            return
        
        item = tree.item(selection[0])
        zanr_id = item['values'][0]
        
        try:
            zanr = self.zanr_dao.get_by_id(zanr_id)
            if not zanr:
                messagebox.showerror("Chyba", "Žánr nenalezen")
                return
        except Exception as e:
            messagebox.showerror("Chyba", str(e))
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Upravit žánr")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Název:*").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nazev_var = tk.StringVar(value=zanr.nazev)
        ttk.Entry(dialog, textvariable=nazev_var
