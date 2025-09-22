#!/usr/bin/env python3
"""
HLAVNÝ ORCHESTRÁTOR: 2-krokový akademický písací proces
Kombinuje tvorbu osnovy (Krok 1) s písaním textu (Krok 2) do jedného nástroja.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from outline_creator_interactive import InteractiveOutlineCreator
from chapter_writer import ChapterWriter
import json
import glob

class AcademicWriter:
    """Hlavný nástroj pre 2-krokový akademický písací proces."""
    
    def __init__(self):
        self.outline_creator = InteractiveOutlineCreator()
        self.chapter_writer = ChapterWriter()
        
    def start(self):
        """Spustí celý 2-krokový proces."""
        
        print("🎓 AKADEMICKÝ PÍSACÍ ASISTENT")
        print("=" * 50)
        print("✨ 2-krokový proces pre kvalitné akademické písanie")
        print("📝 Krok 1: Interaktívna tvorba a korekcia osnovy")
        print("✍️ Krok 2: Písanie kapitoly na základe finalizovanej osnovy")
        print()
        
        while True:
            print("🛠️  HLAVNÉ MENU:")
            print("1. 🆕 Nový projekt (Krok 1 + Krok 2)")
            print("2. 📋 Iba tvorba osnovy (Krok 1)")
            print("3. ✍️ Iba písanie kapitoly (Krok 2)")
            print("4. 📂 Pokračovať v existujúcom projekte")
            print("5. 🗂️ Zobraziť dostupné projekty")
            print("6. 🚪 Ukončiť")
            
            choice = input("\nVyberte možnosť (1-6): ").strip()
            
            if choice == "1":
                self._new_complete_project()
            elif choice == "2":
                self._outline_only()
            elif choice == "3":
                self._writing_only()
            elif choice == "4":
                self._continue_project()
            elif choice == "5":
                self._show_projects()
            elif choice == "6":
                print("👋 Ďakujem za použitie akademického asistenta!")
                break
            else:
                print("❌ Neplatná voľba. Skúste znovu.")
                
            print("\n" + "="*50)
            
    def _new_complete_project(self):
        """Spustí kompletný nový projekt (Krok 1 + 2)."""
        
        print("\n🆕 NOVÝ KOMPLETNÝ PROJEKT")
        print("-" * 30)
        
        # KROK 1: Tvorba osnovy
        print("📋 KROK 1: Tvorba osnovy")
        self.outline_creator.start_interactive_session()
        
        # Nájdi najnovší JSON súbor (osnovu)
        json_files = glob.glob("OSNOVA_*.json")
        if not json_files:
            print("❌ Nenašla sa žiadna JSON osnova!")
            return
            
        latest_json = max(json_files, key=os.path.getctime)
        print(f"\n📂 Použijem osnovu: {latest_json}")
        
        # KROK 2: Písanie kapitoly
        print("\n✍️ KROK 2: Písanie kapitoly")
        if self.chapter_writer.load_outline(latest_json):
            chapter_content = self.chapter_writer.write_chapter()
            
            if chapter_content:
                filename = self.chapter_writer.save_chapter(chapter_content)
                print(f"\n🎉 PROJEKT DOKONČENÝ!")
                print(f"📋 Osnova: {latest_json}")
                print(f"📄 Kapitola: {filename}")
                print(f"📊 Dĺžka: {len(chapter_content.split())} slov")
            else:
                print("❌ Chyba pri generovaní kapitoly!")
                
    def _outline_only(self):
        """Spustí iba tvorbu osnovy."""
        
        print("\n📋 TVORBA OSNOVY (KROK 1)")
        print("-" * 25)
        self.outline_creator.start_interactive_session()
        
    def _writing_only(self):
        """Spustí iba písanie kapitoly."""
        
        print("\n✍️ PÍSANIE KAPITOLY (KROK 2)")
        print("-" * 25)
        
        # Zobraz dostupné JSON súbory
        json_files = glob.glob("OSNOVA_*.json")
        
        if not json_files:
            print("❌ Nenašli sa žiadne JSON osnovy!")
            print("💡 Najprv vytvorte osnovu pomocou Kroku 1.")
            return
            
        print("📂 Dostupné osnovy:")
        for i, json_file in enumerate(json_files, 1):
            # Načítaj základné info
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    topic = data.get('topic', 'Neznáma téma')
                    field = data.get('field', 'Neznámy odbor')
                    pages = data.get('estimated_pages', '?')
                    
                print(f"  {i}. {json_file}")
                print(f"     📚 Téma: {topic}")
                print(f"     🎯 Odbor: {field}")
                print(f"     📄 Strán: {pages}")
                print()
            except:
                print(f"  {i}. {json_file} (chyba pri načítaní)")
                
        # Nech si užívateľ vyberie
        try:
            choice = int(input("Vyberte číslo osnovy: ")) - 1
            if 0 <= choice < len(json_files):
                selected_json = json_files[choice]
                
                if self.chapter_writer.load_outline(selected_json):
                    chapter_content = self.chapter_writer.write_chapter()
                    
                    if chapter_content:
                        filename = self.chapter_writer.save_chapter(chapter_content)
                        print(f"\n✅ Kapitola vytvorená: {filename}")
                        print(f"📊 Dĺžka: {len(chapter_content.split())} slov")
            else:
                print("❌ Neplatný výber!")
        except ValueError:
            print("❌ Zadajte platné číslo!")
            
    def _continue_project(self):
        """Pokračuje v existujúcom projekte."""
        
        print("\n📂 POKRAČOVANIE V PROJEKTE")
        print("-" * 25)
        
        # Zobraz projekty (páry JSON + MD súborov)
        json_files = glob.glob("OSNOVA_*.json")
        
        if not json_files:
            print("❌ Nenašli sa žiadne existujúce projekty!")
            return
            
        print("📁 Existujúce projekty:")
        
        for i, json_file in enumerate(json_files, 1):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    topic = data.get('topic', 'Neznáma téma')
                    
                # Hľadaj príslušnú kapitolu
                topic_clean = topic.replace(' ', '_').replace('/', '_')
                chapter_file = f"KAPITOLA_{topic_clean.upper()}.md"
                
                status = "✅ Hotový" if os.path.exists(chapter_file) else "⏳ Len osnova"
                
                print(f"  {i}. {topic}")
                print(f"     📋 Osnova: {json_file}")
                print(f"     📄 Kapitola: {chapter_file} ({status})")
                print()
            except:
                print(f"  {i}. Chyba pri načítaní {json_file}")
                
        print("🔧 Možnosti:")
        print("1. Upraviť existujúcu osnovu")
        print("2. Vygenerovať kapitolu z osnovy") 
        print("3. Regenerovať existujúcu kapitolu")
        
        action = input("Vyberte akciu (1-3): ").strip()
        
        if action in ["1", "2", "3"]:
            try:
                project_idx = int(input("Vyberte číslo projektu: ")) - 1
                if 0 <= project_idx < len(json_files):
                    selected_json = json_files[project_idx]
                    
                    if action == "1":
                        self._edit_existing_outline(selected_json)
                    elif action == "2":
                        self._generate_from_outline(selected_json)
                    elif action == "3":
                        self._regenerate_chapter(selected_json)
                else:
                    print("❌ Neplatný výber projektu!")
            except ValueError:
                print("❌ Zadajte platné číslo!")
        else:
            print("❌ Neplatná akcia!")
            
    def _show_projects(self):
        """Zobrazí prehľad všetkých projektov."""
        
        print("\n🗂️ PREHĽAD PROJEKTOV")
        print("-" * 20)
        
        json_files = glob.glob("OSNOVA_*.json")
        md_files = glob.glob("KAPITOLA_*.md")
        
        if not json_files and not md_files:
            print("❌ Žiadne projekty nenájdené!")
            return
            
        print(f"📊 Celkovo: {len(json_files)} osnov, {len(md_files)} kapitol")
        print()
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                print(f"📋 {json_file}")
                print(f"   📚 Téma: {data.get('topic', 'N/A')}")
                print(f"   🎯 Odbor: {data.get('field', 'N/A')}")
                print(f"   📄 Strán: {data.get('estimated_pages', 'N/A')}")
                print(f"   📖 Zdrojov: {data.get('estimated_sources', {}).get('total_recommended', 'N/A')}")
                print(f"   📅 Vytvorené: {data.get('generated_at', 'N/A')[:10]}")
                
                # Skontroluj príslušnú kapitolu
                topic_clean = data.get('topic', '').replace(' ', '_').replace('/', '_')
                chapter_file = f"KAPITOLA_{topic_clean.upper()}.md"
                
                if os.path.exists(chapter_file):
                    stat = os.path.getsize(chapter_file)
                    print(f"   ✅ Kapitola: {chapter_file} ({stat} B)")
                else:
                    print(f"   ⏳ Kapitola: Nie je vytvorená")
                    
                print()
            except Exception as e:
                print(f"❌ Chyba pri čítaní {json_file}: {e}")
                print()
                
    def _edit_existing_outline(self, json_file):
        """Upraví existujúcu osnovu."""
        
        print(f"\n📝 Úprava osnovy: {json_file}")
        # Tu by sa dala implementovať editácia existujúcej osnovy
        # Pre teraz len informácia
        print("💡 Táto funkcia bude implementovaná v budúcnosti.")
        print("🔧 Zatiaľ vytvorte novú osnovu alebo upravte JSON súbor manuálne.")
        
    def _generate_from_outline(self, json_file):
        """Vygeneruje kapitolu z osnovy."""
        
        if self.chapter_writer.load_outline(json_file):
            chapter_content = self.chapter_writer.write_chapter()
            
            if chapter_content:
                filename = self.chapter_writer.save_chapter(chapter_content)
                print(f"\n✅ Kapitola vytvorená: {filename}")
                
    def _regenerate_chapter(self, json_file):
        """Regeneruje existujúcu kapitolu."""
        
        print(f"\n🔄 Regenerujem kapitolu z: {json_file}")
        
        if self.chapter_writer.load_outline(json_file):
            chapter_content = self.chapter_writer.write_chapter()
            
            if chapter_content:
                filename = self.chapter_writer.save_chapter(chapter_content)
                print(f"\n✅ Kapitola regenerovaná: {filename}")
                print("⚠️ Starý obsah bol prepísaný!")

def main():
    """Hlavná funkcia."""
    
    writer = AcademicWriter()
    writer.start()

if __name__ == "__main__":
    main()