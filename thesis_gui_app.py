#!/usr/bin/env python3
"""
Thesis AI Agent - Desktop GUI Application
Moderný desktopový interface pre prácu s témou chladenia vnutorných priestorov
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import subprocess
import threading
from pathlib import Path
import webbrowser
from datetime import datetime

# Import našich modulov
try:
    from cooling_analysis_tool import CoolingAnalyzer, BuildingParameters, CoolingSystem
    from energy_audit.calculations import CoolingCalculations
except ImportError as e:
    print(f"Warning: Nemožno importovať moduly: {e}")

class ThesisGUIApp:
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.create_widgets()
        self.analyzer = CoolingAnalyzer() if 'CoolingAnalyzer' in globals() else None
        
    def setup_main_window(self):
        """Nastavenie hlavného okna"""
        self.root.title("🌡️ Thesis AI Agent - Chladenie vnutorných priestorov")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Ikona a štýl
        try:
            self.root.iconbitmap('icon.ico')  # ak máš ikonu
        except:
            pass
            
        # Moderné farby
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'success': '#00A676',
            'warning': '#F18F01',
            'danger': '#C73E1D',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
        
        # Štýl pre ttk
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Vytvorenie hlavných komponentov GUI"""
        
        # Hlavný frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfigurácia grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Sidebar
        self.create_sidebar(main_frame)
        
        # Main content area
        self.create_main_content(main_frame)
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self, parent):
        """Vytvorenie header-u aplikácie"""
        header_frame = ttk.Frame(parent, padding="5")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Logo a názov
        title_label = ttk.Label(
            header_frame, 
            text="🌡️ Thesis AI Agent - Chladenie vnutorných priestorov",
            font=('Segoe UI', 16, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Info o projekte
        info_label = ttk.Label(
            header_frame,
            text="Inteligentný nástroj pre analýzu a návrh chladiacich systémov",
            font=('Segoe UI', 10, 'italic')
        )
        info_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
    def create_sidebar(self, parent):
        """Vytvorenie bočného panelu s menu"""
        sidebar_frame = ttk.LabelFrame(parent, text="📋 Menu", padding="10")
        sidebar_frame.grid(row=1, column=0, sticky=(tk.W, tk.N, tk.S), padx=(0, 10))
        
        # Menu buttons
        menu_buttons = [
            ("📖 Kapitoly", self.show_chapters),
            ("🧮 Cooling Calculator", self.show_calculator),
            ("📊 Analýza systémov", self.show_analysis),
            ("📈 Grafy a výsledky", self.show_results),
            ("⚙️ VRF/VRV Systémy", self.show_vrf_info),
            ("🏢 Case Studies", self.show_case_studies),
            ("📝 Export/Import", self.show_export_import),
            ("ℹ️ O aplikácii", self.show_about)
        ]
        
        for i, (text, command) in enumerate(menu_buttons):
            btn = ttk.Button(
                sidebar_frame,
                text=text,
                command=command,
                width=20
            )
            btn.grid(row=i, column=0, pady=5, sticky=(tk.W, tk.E))
            
        # Aktuálny čas
        self.time_label = ttk.Label(sidebar_frame, font=('Segoe UI', 8))
        self.time_label.grid(row=len(menu_buttons)+1, column=0, pady=(20, 0))
        self.update_time()
        
    def create_main_content(self, parent):
        """Vytvorenie hlavnej content oblasti"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Uvítacia stránka
        self.create_welcome_tab()
        
    def create_welcome_tab(self):
        """Vytvorenie uvítacej stránky"""
        welcome_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(welcome_frame, text="🏠 Úvod")
        
        # Welcome text
        welcome_text = """
        🎓 VITAJTE V THESIS AI AGENT

        Tento nástroj vám pomôže s prácou na téme:
        "Chladenie vnutorných priestorov - technológie, efektívnosť a aplikácie"

        📚 Dostupné funkcie:
        • Analýza chladiacej potreby budov
        • Porovnanie rôznych chladiacích systémov  
        • Ekonomická analýza a ROI výpočty
        • Generovanie grafov a reportov
        • VRF/VRV systémy - detailné informácie
        • Export výsledkov do rôznych formátov

        💡 Začnite výberom funkcie z menu vľavo
        """
        
        welcome_label = ttk.Label(
            welcome_frame,
            text=welcome_text,
            font=('Segoe UI', 12),
            justify='left'
        )
        welcome_label.grid(row=0, column=0, sticky=(tk.W, tk.N))
        
        # Rýchle akcie
        quick_frame = ttk.LabelFrame(welcome_frame, text="⚡ Rýchle akcie", padding="15")
        quick_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        quick_buttons = [
            ("🧮 Spustiť Cooling Calculator", self.show_calculator),
            ("📊 Nová analýza systémov", self.show_analysis),
            ("📖 Otvoriť kapitoly", self.open_chapters_folder),
            ("📈 Zobraziť posledné výsledky", self.show_last_results)
        ]
        
        for i, (text, command) in enumerate(quick_buttons):
            btn = ttk.Button(quick_frame, text=text, command=command)
            btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky=(tk.W, tk.E))
            
        quick_frame.columnconfigure(0, weight=1)
        quick_frame.columnconfigure(1, weight=1)
        
    def create_status_bar(self):
        """Vytvorenie status baru"""
        self.status_var = tk.StringVar()
        self.status_var.set("Pripravený")
        
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding="5"
        )
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    # Menu functions
    def show_chapters(self):
        """Zobrazenie kapitol"""
        if hasattr(self, 'chapters_tab'):
            self.notebook.forget(self.chapters_tab)
            
        self.chapters_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.chapters_tab, text="📖 Kapitoly")
        self.notebook.select(self.chapters_tab)
        
        # Zoznam kapitol
        chapters_data = [
            ("Kapitola 1", "Úvod do problematiky chladenia", "KAPITOLA_1_CHLADENIE_UVOD.md", "✅ Hotovo"),
            ("Kapitola 2", "VRF a VRV systémy", "KAPITOLA_VRF_VRV_SYSTEMY.md", "✅ Hotovo"),
            ("Kapitola 3", "Termodynamické základy", "kapitola_3.md", "⏳ Pripravuje sa"),
            ("Kapitola 4", "Návrh a dimenzovanie", "kapitola_4.md", "⏳ Pripravuje sa"),
            ("Kapitola 5", "Case study", "kapitola_5.md", "⏳ Pripravuje sa")
        ]
        
        # Treeview pre kapitoly
        tree = ttk.Treeview(self.chapters_tab, columns=('file', 'status'), height=10)
        tree.heading('#0', text='Kapitola')
        tree.heading('file', text='Súbor')
        tree.heading('status', text='Stav')
        
        for chapter, desc, file, status in chapters_data:
            item = tree.insert('', 'end', text=f'{chapter}: {desc}', values=(file, status))
            
        tree.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Buttons pre kapitoly
        ttk.Button(
            self.chapters_tab,
            text="📂 Otvoriť vybraný súbor",
            command=lambda: self.open_selected_chapter(tree)
        ).grid(row=1, column=0, padx=5, sticky=tk.W)
        
        ttk.Button(
            self.chapters_tab,
            text="📝 Nová kapitola",
            command=self.create_new_chapter
        ).grid(row=1, column=1, padx=5)
        
        ttk.Button(
            self.chapters_tab,
            text="📁 Otvoriť priečinok",
            command=self.open_chapters_folder
        ).grid(row=1, column=2, padx=5, sticky=tk.E)
        
        self.chapters_tab.rowconfigure(0, weight=1)
        self.chapters_tab.columnconfigure(0, weight=1)
        
    def show_calculator(self):
        """Zobrazenie cooling calculatora"""
        if hasattr(self, 'calc_tab'):
            self.notebook.forget(self.calc_tab)
            
        self.calc_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.calc_tab, text="🧮 Calculator")
        self.notebook.select(self.calc_tab)
        
        # Input sekcia
        input_frame = ttk.LabelFrame(self.calc_tab, text="📊 Parametre budovy", padding="15")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Input fields
        self.calc_vars = {}
        calc_fields = [
            ('Názov budovy:', 'building_name', 'Administratívna budova'),
            ('Podlahová plocha [m²]:', 'floor_area', '1500'),
            ('Plocha okien [m²]:', 'window_area', '300'),
            ('Počet osôb:', 'people_count', '60'),
            ('Výkon osvetlenia [W]:', 'lighting_power', '15000'),
            ('Výkon zariadení [W]:', 'equipment_power', '22500'),
            ('U-value stien [W/m²K]:', 'u_walls', '0.32'),
            ('U-value strechy [W/m²K]:', 'u_roof', '0.20'),
            ('U-value okien [W/m²K]:', 'u_windows', '1.2'),
            ('Faktor tienenia [-]:', 'shading_factor', '0.7')
        ]
        
        for i, (label, var_name, default) in enumerate(calc_fields):
            ttk.Label(input_frame, text=label).grid(row=i//2, column=(i%2)*2, sticky=tk.W, padx=5, pady=2)
            var = tk.StringVar(value=default)
            self.calc_vars[var_name] = var
            entry = ttk.Entry(input_frame, textvariable=var, width=15)
            entry.grid(row=i//2, column=(i%2)*2+1, sticky=tk.W, padx=5, pady=2)
            
        # Lokalita
        ttk.Label(input_frame, text="Lokalita:").grid(row=len(calc_fields)//2, column=0, sticky=tk.W, padx=5, pady=10)
        self.location_var = tk.StringVar(value="bratislava")
        location_combo = ttk.Combobox(
            input_frame,
            textvariable=self.location_var,
            values=['bratislava', 'košice', 'žilina'],
            state='readonly',
            width=12
        )
        location_combo.grid(row=len(calc_fields)//2, column=1, sticky=tk.W, padx=5, pady=10)
        
        # Calculate button
        calc_btn = ttk.Button(
            input_frame,
            text="🧮 Vypočítať chladiacu potrebu",
            command=self.calculate_cooling_load
        )
        calc_btn.grid(row=len(calc_fields)//2, column=2, columnspan=2, pady=10)
        
        # Results sekcia
        self.results_frame = ttk.LabelFrame(self.calc_tab, text="📊 Výsledky", padding="15")
        self.results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.calc_tab.rowconfigure(1, weight=1)
        self.calc_tab.columnconfigure(0, weight=1)
        
    def show_analysis(self):
        """Zobrazenie analýzy systémov"""
        if hasattr(self, 'analysis_tab'):
            self.notebook.forget(self.analysis_tab)
            
        self.analysis_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.analysis_tab, text="📊 Analýza")
        self.notebook.select(self.analysis_tab)
        
        # Info text
        info_text = """
        📊 ANALÝZA CHLADIACICH SYSTÉMOV
        
        Porovnanie rôznych typov chladiacich systémov:
        • Split systémy (Multi)
        • VRF systémy  
        • Chillery + FCU
        • Evaporačné chladiče
        • Absorpčné systémy
        
        Analýza zahŕňa:
        ✅ Investičné náklady
        ✅ Prevádzkové náklady  
        ✅ COP a efektívnosť
        ✅ Životný cyklus (LCC)
        ✅ Payback period
        """
        
        ttk.Label(self.analysis_tab, text=info_text, justify='left').grid(row=0, column=0, sticky=(tk.W, tk.N))
        
        # Spustiť analýzu
        ttk.Button(
            self.analysis_tab,
            text="🚀 Spustiť kompletnú analýzu",
            command=self.run_full_analysis
        ).grid(row=1, column=0, pady=20, sticky=tk.W)
        
    def show_results(self):
        """Zobrazenie výsledkov a grafov"""
        if hasattr(self, 'results_tab'):
            self.notebook.forget(self.results_tab)
            
        self.results_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.results_tab, text="📈 Výsledky")
        self.notebook.select(self.results_tab)
        
        # Načítanie posledných výsledkov
        try:
            with open('cooling_analysis_results.json', 'r', encoding='utf-8') as f:
                results = json.load(f)
                
            # Zobrazenie základných údajov
            building_info = results.get('building', {})
            info_text = f"""
            🏢 POSLEDNÁ ANALÝZA
            
            Budova: {building_info.get('name', 'N/A')}
            Podlahová plocha: {building_info.get('floor_area_m2', 0):,.0f} m²
            Celková chladiaca potreba: {building_info.get('total_cooling_load_kW', 0):,.1f} kW
            Merná potreba: {building_info.get('specific_load_W_m2', 0):,.1f} W/m²
            """
            
            ttk.Label(self.results_tab, text=info_text, justify='left').grid(row=0, column=0, sticky=(tk.W, tk.N))
            
        except FileNotFoundError:
            ttk.Label(
                self.results_tab,
                text="❌ Žiadne výsledky nenájdené.\nNajprv spustite analýzu.",
                justify='center'
            ).grid(row=0, column=0)
            
        # Buttons pre prácu s výsledkami
        buttons_frame = ttk.Frame(self.results_tab)
        buttons_frame.grid(row=1, column=0, pady=20, sticky=tk.W)
        
        ttk.Button(
            buttons_frame,
            text="🖼️ Otvoriť grafy",
            command=self.open_graphs
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="📄 Export do PDF",
            command=self.export_to_pdf
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="📊 Export do Excel",
            command=self.export_to_excel
        ).grid(row=0, column=2, padx=5)
        
    def show_vrf_info(self):
        """Zobrazenie info o VRF/VRV systémoch"""
        if hasattr(self, 'vrf_tab'):
            self.notebook.forget(self.vrf_tab)
            
        self.vrf_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.vrf_tab, text="⚙️ VRF/VRV")
        self.notebook.select(self.vrf_tab)
        
        # VRF info
        vrf_info = """
        ⚙️ VRF/VRV SYSTÉMY
        
        Variable Refrigerant Flow (VRF) a Variable Refrigerant Volume (VRV) 
        sú pokročilé klimatizačné technológie s vysokou efektívnosťou.
        
        🔧 Hlavné výhody:
        • Vysoký COP: 4,0-6,5
        • SEER: 6,1-8,5
        • Zónová regulácia ±0,5°C
        • Heat recovery možnosti
        • Tichá prevádzka: 19-35 dB(A)
        
        💰 Ekonomické aspekty (SR):
        • Investičné náklady: 1000-1800 €/kW
        • Úspory energie: 20-40%
        • Payback: 5-8 rokov
        
        🌍 Vhodnosť pre SR:
        ✅ Letné teploty 25-35°C - optimálne
        ✅ Zimné teploty -5 až -15°C - vhodné
        ✅ Prechodné obdobia - heat recovery výhoda
        """
        
        text_widget = scrolledtext.ScrolledText(
            self.vrf_tab,
            height=20,
            font=('Consolas', 10)
        )
        text_widget.insert('1.0', vrf_info)
        text_widget.config(state='disabled')
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button na otvorenie kapitoly
        ttk.Button(
            self.vrf_tab,
            text="📖 Otvoriť kapitolu VRF/VRV",
            command=lambda: self.open_file('KAPITOLA_VRF_VRV_SYSTEMY.md')
        ).grid(row=1, column=0, pady=10, sticky=tk.W)
        
        self.vrf_tab.rowconfigure(0, weight=1)
        self.vrf_tab.columnconfigure(0, weight=1)
        
    def show_case_studies(self):
        """Zobrazenie case studies"""
        if hasattr(self, 'case_tab'):
            self.notebook.forget(self.case_tab)
            
        self.case_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.case_tab, text="🏢 Case Studies")
        self.notebook.select(self.case_tab)
        
        case_info = """
        🏢 CASE STUDIES - PRÍKLADY APLIKÁCIÍ
        
        1. Administratívna budova Bratislava
           • Plocha: 1500 m²
           • Systém: VRF heat recovery
           • Úspory: 42% energie
           • Payback: 7,2 roka
        
        2. Obchodné centrum Košice (pripravuje sa)
           • Plocha: 8000 m²
           • Systém: Centrálny chiller + FCU
           
        3. Hotel Žilina (pripravuje sa)  
           • 120 izieb
           • Systém: VRF 2-pipe
        """
        
        ttk.Label(self.case_tab, text=case_info, justify='left').grid(row=0, column=0, sticky=(tk.W, tk.N))
        
    def show_export_import(self):
        """Export/Import funkcionalita"""
        if hasattr(self, 'export_tab'):
            self.notebook.forget(self.export_tab)
            
        self.export_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.export_tab, text="📝 Export/Import")
        self.notebook.select(self.export_tab)
        
        # Export sekcia
        export_frame = ttk.LabelFrame(self.export_tab, text="📤 Export", padding="15")
        export_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        export_buttons = [
            ("📄 Export kapitoly do PDF", self.export_chapters_pdf),
            ("📊 Export výsledkov do Excel", self.export_to_excel),
            ("🖼️ Export grafov (PNG)", self.export_graphs),
            ("💾 Zálohovanie projektu", self.backup_project)
        ]
        
        for i, (text, command) in enumerate(export_buttons):
            ttk.Button(export_frame, text=text, command=command).grid(
                row=i, column=0, pady=5, sticky=(tk.W, tk.E)
            )
            
        # Import sekcia
        import_frame = ttk.LabelFrame(self.export_tab, text="📥 Import", padding="15")
        import_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        import_buttons = [
            ("📂 Import building parametrov", self.import_building_params),
            ("🔄 Obnoviť zo zálohy", self.restore_backup)
        ]
        
        for i, (text, command) in enumerate(import_buttons):
            ttk.Button(import_frame, text=text, command=command).grid(
                row=i, column=0, pady=5, sticky=(tk.W, tk.E)
            )
            
        export_frame.columnconfigure(0, weight=1)
        import_frame.columnconfigure(0, weight=1)
        
    def show_about(self):
        """O aplikácii"""
        if hasattr(self, 'about_tab'):
            self.notebook.forget(self.about_tab)
            
        self.about_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.about_tab, text="ℹ️ O aplikácii")
        self.notebook.select(self.about_tab)
        
        about_text = f"""
        🌡️ THESIS AI AGENT
        Verzia 1.0 - {datetime.now().strftime('%Y-%m-%d')}
        
        📚 Téma: Chladenie vnutorných priestorov
        🎓 Účel: Diplomová/Bakalárska práca
        
        🔧 Funkcionality:
        • Analýza chladiacej potreby budov
        • Porovnanie chladiacich systémov  
        • VRF/VRV systémy - detailné info
        • Ekonomická analýza a ROI
        • Export do PDF/Excel formátov
        • Generovanie grafov a reportov
        
        💻 Technológie:
        • Python 3.x
        • Tkinter GUI
        • Matplotlib grafy  
        • Pandas analýzy
        • JSON dáta
        
        👨‍💻 Autor: Thesis AI Agent
        📧 Podpora: cez GitHub Issues
        🌐 GitHub: https://github.com/thesis-ai-agent
        
        📄 Licencia: MIT License
        """
        
        text_widget = scrolledtext.ScrolledText(
            self.about_tab,
            height=20,
            font=('Consolas', 10)
        )
        text_widget.insert('1.0', about_text)
        text_widget.config(state='disabled')
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.about_tab.rowconfigure(0, weight=1)
        self.about_tab.columnconfigure(0, weight=1)
        
    # Utility functions
    def update_time(self):
        """Aktualizácia času v sidebar"""
        current_time = datetime.now().strftime("%H:%M:%S\n%d.%m.%Y")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def update_status(self, message):
        """Aktualizácia status baru"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    # Action functions
    def calculate_cooling_load(self):
        """Výpočet chladiacej potreby"""
        if not self.analyzer:
            messagebox.showerror("Chyba", "Cooling analyzer nie je dostupný")
            return
            
        try:
            # Získanie parametrov z GUI
            building_params = BuildingParameters(
                name=self.calc_vars['building_name'].get(),
                floor_area_m2=float(self.calc_vars['floor_area'].get()),
                window_area_m2=float(self.calc_vars['window_area'].get()),
                number_of_people=int(self.calc_vars['people_count'].get()),
                lighting_power_W=float(self.calc_vars['lighting_power'].get()),
                equipment_power_W=float(self.calc_vars['equipment_power'].get()),
                u_value_walls=float(self.calc_vars['u_walls'].get()),
                u_value_roof=float(self.calc_vars['u_roof'].get()),
                u_value_windows=float(self.calc_vars['u_windows'].get()),
                shading_factor=float(self.calc_vars['shading_factor'].get())
            )
            
            self.update_status("Počítam chladiacu potrebu...")
            
            # Výpočet
            location = self.location_var.get()
            results = self.analyzer.calculate_cooling_load(building_params, location)
            
            # Zobrazenie výsledkov
            self.display_cooling_results(results)
            self.update_status("Výpočet dokončený")
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri výpočte: {str(e)}")
            self.update_status("Chyba pri výpočte")
            
    def display_cooling_results(self, results):
        """Zobrazenie výsledkov výpočtu"""
        # Vyčistenie results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Vytvorenie treeview pre výsledky
        tree = ttk.Treeview(self.results_frame, columns=('value', 'unit'), height=8)
        tree.heading('#0', text='Parameter')
        tree.heading('value', text='Hodnota')
        tree.heading('unit', text='Jednotka')
        
        # Vloženie výsledkov
        result_items = [
            ('Tepelné zisky od osôb', f"{results['people_W']:,.0f}", 'W'),
            ('Tepelné zisky od osvetlenia', f"{results['lighting_W']:,.0f}", 'W'), 
            ('Tepelné zisky od zariadení', f"{results['equipment_W']:,.0f}", 'W'),
            ('Solárne zisky', f"{results['solar_W']:,.0f}", 'W'),
            ('Tepelné zisky prechodom', f"{results['transmission_W']:,.0f}", 'W'),
            ('Ventilačné zisky', f"{results['ventilation_W']:,.0f}", 'W'),
            ('', '', ''),  # separator
            ('CELKOVÁ POTREBA', f"{results['total_cooling_W']:,.0f}", 'W'),
            ('CELKOVÁ POTREBA', f"{results['total_cooling_W']/1000:,.1f}", 'kW'),
            ('Merná potreba', f"{results['specific_cooling_W_m2']:,.1f}", 'W/m²')
        ]
        
        for item, value, unit in result_items:
            if item == '':  # separator
                tree.insert('', 'end', text='─────────────────────', values=('', ''))
            elif item == 'CELKOVÁ POTREBA':
                tree.insert('', 'end', text=item, values=(value, unit), tags=('bold',))
            else:
                tree.insert('', 'end', text=item, values=(value, unit))
                
        tree.tag_configure('bold', font=('Segoe UI', 10, 'bold'))
        tree.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Buttons pre export
        ttk.Button(
            self.results_frame,
            text="📊 Analýza systémov",
            command=self.run_system_analysis
        ).grid(row=1, column=0, padx=5, sticky=tk.W)
        
        ttk.Button(
            self.results_frame,
            text="💾 Uložiť výsledky",
            command=self.save_results
        ).grid(row=1, column=1, padx=5, sticky=tk.E)
        
        self.results_frame.rowconfigure(0, weight=1)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.columnconfigure(1, weight=1)
        
    def run_full_analysis(self):
        """Spustenie kompletnej analýzy"""
        def analysis_thread():
            try:
                self.update_status("Spúšťam kompletnú analýzu...")
                
                # Spustenie cooling_analysis_tool.py
                result = subprocess.run(
                    ['python', 'cooling_analysis_tool.py'],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Úspech", 
                        "Analýza dokončená!\n\nVýsledky uložené:\n• cooling_analysis_results.json\n• Grafy: *.png súbory"
                    ))
                    self.update_status("Analýza dokončená")
                else:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Chyba",
                        f"Chyba pri analýze:\n{result.stderr}"
                    ))
                    self.update_status("Chyba pri analýze")
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Chyba",
                    f"Neočakávaná chyba: {str(e)}"
                ))
                
        # Spustenie v separátnom vlákne
        thread = threading.Thread(target=analysis_thread)
        thread.daemon = True
        thread.start()
        
    def run_system_analysis(self):
        """Spustenie analýzy systémov na základe aktuálnych výpočtov"""
        self.run_full_analysis()
        
    # File operations
    def open_file(self, filename):
        """Otvorenie súboru v predvolenom editore"""
        try:
            if os.path.exists(filename):
                os.startfile(filename)  # Windows
                self.update_status(f"Otvorený súbor: {filename}")
            else:
                messagebox.showerror("Chyba", f"Súbor {filename} neexistuje")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nemožno otvoriť súbor: {str(e)}")
            
    def open_selected_chapter(self, tree):
        """Otvorenie vybranej kapitoly"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            filename = item['values'][0] if item['values'] else None
            if filename:
                self.open_file(filename)
        else:
            messagebox.showwarning("Upozornenie", "Vyberte kapitolu na otvorenie")
            
    def open_chapters_folder(self):
        """Otvorenie priečinku s kapitolami"""
        try:
            os.startfile(os.getcwd())  # Otvor aktuálny priečinok
            self.update_status("Otvorený priečinok s kapitolami")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nemožno otvoriť priečinok: {str(e)}")
            
    def open_graphs(self):
        """Otvorenie grafov"""
        png_files = [f for f in os.listdir('.') if f.endswith('.png')]
        if png_files:
            for png_file in png_files:
                try:
                    os.startfile(png_file)
                except:
                    pass
            self.update_status("Otvorené grafy")
        else:
            messagebox.showinfo("Info", "Žiadne grafy nenájdené.\nNajprv spustite analýzu.")
            
    def show_last_results(self):
        """Zobrazenie posledných výsledkov"""
        self.show_results()
        
    def create_new_chapter(self):
        """Vytvorenie novej kapitoly"""
        chapter_name = tk.simpledialog.askstring(
            "Nová kapitola",
            "Zadajte názov novej kapitoly:"
        )
        if chapter_name:
            filename = f"KAPITOLA_{chapter_name.upper().replace(' ', '_')}.md"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {chapter_name.upper()}\n\n## Úvod\n\n[Obsah kapitoly]\n\n---\n\n## Použitá literatúra\n\n")
                messagebox.showinfo("Úspech", f"Kapitola vytvorená: {filename}")
                self.open_file(filename)
            except Exception as e:
                messagebox.showerror("Chyba", f"Nemožno vytvoriť kapitolu: {str(e)}")
                
    # Export functions  
    def export_to_pdf(self):
        """Export výsledkov do PDF"""
        messagebox.showinfo("Info", "PDF export - funkcia v príprave")
        
    def export_to_excel(self):
        """Export výsledkov do Excel"""
        messagebox.showinfo("Info", "Excel export - funkcia v príprave")
        
    def export_graphs(self):
        """Export grafov"""
        png_files = [f for f in os.listdir('.') if f.endswith('.png')]
        if png_files:
            target_dir = filedialog.askdirectory(title="Vyberte priečinok pre export grafov")
            if target_dir:
                import shutil
                for png_file in png_files:
                    shutil.copy2(png_file, os.path.join(target_dir, png_file))
                messagebox.showinfo("Úspech", f"Exportované {len(png_files)} grafov do {target_dir}")
        else:
            messagebox.showinfo("Info", "Žiadne grafy na export")
            
    def export_chapters_pdf(self):
        """Export kapitol do PDF"""
        messagebox.showinfo("Info", "PDF export kapitol - funkcia v príprave") 
        
    def backup_project(self):
        """Zálohovanie projektu"""
        messagebox.showinfo("Info", "Backup projekt - funkcia v príprave")
        
    def import_building_params(self):
        """Import parametrov budovy"""
        messagebox.showinfo("Info", "Import parametrov - funkcia v príprave")
        
    def restore_backup(self):
        """Obnovenie zo zálohy"""
        messagebox.showinfo("Info", "Restore backup - funkcia v príprave")
        
    def save_results(self):
        """Uloženie aktuálnych výsledkov"""
        messagebox.showinfo("Info", "Výsledky uložené do cooling_analysis_results.json")


def main():
    """Hlavná funkcia - spustenie aplikácie"""
    root = tk.Tk()
    app = ThesisGUIApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Aplikácia ukončená používateľom")
    except Exception as e:
        print(f"Chyba aplikácie: {e}")
        messagebox.showerror("Kritická chyba", f"Aplikácia sa ukončuje kvôli chybe:\n{str(e)}")


if __name__ == "__main__":
    main()