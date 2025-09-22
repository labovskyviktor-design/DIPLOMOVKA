#!/usr/bin/env python3
"""
KROK 1: Interaktívny tvorba a korekcia osnovy
Umožňuje užívateľovi vytvoriť, upraviť a zdokonaliť osnovu pred písaním textu.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from outline_planner import OutlinePlanner
import json
from datetime import datetime

class InteractiveOutlineCreator:
    """Interaktívny nástroj pre tvorbu a korekciu osnov."""
    
    def __init__(self):
        self.planner = OutlinePlanner()
        self.current_outline = None
        
    def start_interactive_session(self):
        """Spustí interaktívnu session pre tvorbu osnovy."""
        
        print("🎓 KROK 1: TVORBA A KOREKCIA OSNOVY")
        print("=" * 60)
        print("📝 Tento nástroj vám pomôže vytvoriť dokonalú osnovu pred písaním")
        print("🔧 Môžete upravovať, pridávať a mazať sekcie podľa potreby")
        print()
        
        # Získaj tému
        topic = input("📚 Zadajte tému vašej kapitoly: ").strip()
        if not topic:
            print("❌ Téma nemôže byť prázdna!")
            return
            
        # Detekuj/vyber odbor
        field = self._select_field(topic)
        
        # Vygeneruj počiatočnú osnovu
        print(f"\n🎯 Generujem osnovu pre tému: '{topic}'")
        self.current_outline = self.planner.generate_outline(topic, field)
        
        # Interaktívne menu
        self._interactive_menu()
        
    def _select_field(self, topic):
        """Umožní užívateľovi vybrať alebo potvrdiť odbor."""
        
        detected = self.planner.detect_field(topic)
        print(f"\n🔍 Detekovaný odbor: {detected}")
        
        print("\n🔧 Chcete zmeniť odbor?")
        print("1. Technické/Inžinierske vedy")
        print("2. Pedagogické/Humanitné vedy")
        print("3. Ekonomické/Obchodné vedy")
        print("4. Použiť detekovaný odbor")
        
        choice = input("\nVaša voľba (1-4): ").strip()
        
        field_mapping = {
            "1": "technical",
            "2": "pedagogical",
            "3": "economic",
            "4": detected
        }
        
        return field_mapping.get(choice, detected)
    
    def _interactive_menu(self):
        """Hlavné interaktívne menu pre úpravu osnovy."""
        
        while True:
            self._display_current_outline()
            
            print("\n🛠️  MOŽNOSTI ÚPRAV:")
            print("1. 📝 Upraviť názov sekcie")
            print("2. ➕ Pridať novú podsekciu")
            print("3. ❌ Odstrániť podsekciu")
            print("4. 📊 Zmeniť odhady (strany, zdroje)")
            print("5. 🔄 Regenerovať sekciu")
            print("6. 💾 Uložiť a pokračovať na písanie")
            print("7. 🚪 Ukončiť bez uloženia")
            
            choice = input("\nVyberte možnosť (1-7): ").strip()
            
            if choice == "1":
                self._edit_section_title()
            elif choice == "2":
                self._add_subsection()
            elif choice == "3":
                self._remove_subsection()
            elif choice == "4":
                self._edit_estimates()
            elif choice == "5":
                self._regenerate_section()
            elif choice == "6":
                self._save_and_continue()
                break
            elif choice == "7":
                print("👋 Ukončujem bez uloženia...")
                break
            else:
                print("❌ Neplatná voľba. Skúste znovu.")
                
    def _display_current_outline(self):
        """Zobrazí súčasnú osnovu."""
        
        print("\n📋 SÚČASNÁ OSNOVA:")
        print("=" * 50)
        print(f"📚 Téma: {self.current_outline['topic']}")
        print(f"🎯 Odbor: {self.current_outline['field']}")
        print(f"📄 Odhadované strany: {self.current_outline['estimated_pages']}")
        print(f"📖 Odhadované zdroje: {self.current_outline['estimated_sources']['total_recommended']}")
        print()
        
        for i, section in enumerate(self.current_outline['sections'], 1):
            print(f"📁 {section['id']}. {section['title']}")
            print(f"   📄 ~{section.get('estimated_pages', 6)} strán")
            
            for j, subsection in enumerate(section['subsections'], 1):
                print(f"   {section['id']}.{j} {subsection}")
                
            print()
            
    def _edit_section_title(self):
        """Umožní úpravu názvu sekcie."""
        
        section_id = input("\n🔧 Zadajte číslo sekcie na úpravu (1-5): ").strip()
        
        try:
            idx = int(section_id) - 1
            if 0 <= idx < len(self.current_outline['sections']):
                section = self.current_outline['sections'][idx]
                print(f"\n📝 Súčasný názov: {section['title']}")
                new_title = input("✏️ Nový názov: ").strip()
                
                if new_title:
                    section['title'] = new_title
                    print("✅ Názov sekcie bol zmenený!")
                else:
                    print("❌ Názov nemôže byť prázdny!")
            else:
                print("❌ Neplatné číslo sekcie!")
        except ValueError:
            print("❌ Zadajte platné číslo!")
            
    def _add_subsection(self):
        """Pridá novú podsekciu do vybranej sekcie."""
        
        section_id = input("\n➕ Zadajte číslo sekcie (1-5): ").strip()
        
        try:
            idx = int(section_id) - 1
            if 0 <= idx < len(self.current_outline['sections']):
                section = self.current_outline['sections'][idx]
                new_subsection = input("📝 Názov novej podsekcie: ").strip()
                
                if new_subsection:
                    section['subsections'].append(new_subsection)
                    # Prepočítaj odhad strán
                    section['estimated_pages'] = len(section['subsections']) * 2
                    print("✅ Podsekcia bola pridaná!")
                else:
                    print("❌ Názov nemôže byť prázdny!")
            else:
                print("❌ Neplatné číslo sekcie!")
        except ValueError:
            print("❌ Zadajte platné číslo!")
            
    def _remove_subsection(self):
        """Odstráni podsekciu."""
        
        section_id = input("\n❌ Zadajte číslo sekcie (1-5): ").strip()
        
        try:
            idx = int(section_id) - 1
            if 0 <= idx < len(self.current_outline['sections']):
                section = self.current_outline['sections'][idx]
                
                print(f"\n📋 Podsekcie v sekcii {section_id}:")
                for i, subsection in enumerate(section['subsections'], 1):
                    print(f"  {i}. {subsection}")
                
                sub_idx = input("\n🗑️ Číslo podsekcie na odstránenie: ").strip()
                sub_idx = int(sub_idx) - 1
                
                if 0 <= sub_idx < len(section['subsections']):
                    removed = section['subsections'].pop(sub_idx)
                    section['estimated_pages'] = len(section['subsections']) * 2
                    print(f"✅ Podsekcia '{removed}' bola odstránená!")
                else:
                    print("❌ Neplatné číslo podsekcie!")
            else:
                print("❌ Neplatné číslo sekcie!")
        except ValueError:
            print("❌ Zadajte platné číslo!")
            
    def _edit_estimates(self):
        """Umožní úpravu odhadov strán a zdrojov."""
        
        print("\n📊 ÚPRAVA ODHADOV:")
        print(f"Súčasné odhady: {self.current_outline['estimated_pages']} strán, "
              f"{self.current_outline['estimated_sources']['total_recommended']} zdrojov")
        
        try:
            new_pages = input("📄 Nový odhad strán (Enter = bez zmeny): ").strip()
            if new_pages:
                self.current_outline['estimated_pages'] = int(new_pages)
                
            new_sources = input("📚 Nový odhad zdrojov (Enter = bez zmeny): ").strip()
            if new_sources:
                sources = int(new_sources)
                self.current_outline['estimated_sources']['total_recommended'] = sources
                self.current_outline['estimated_sources']['total_minimum'] = int(sources * 0.8)
                
            print("✅ Odhady boli aktualizované!")
            
        except ValueError:
            print("❌ Zadajte platné čísla!")
            
    def _regenerate_section(self):
        """Regeneruje obsah vybranej sekcie."""
        
        section_id = input("\n🔄 Zadajte číslo sekcie na regeneráciu (1-5): ").strip()
        
        try:
            idx = int(section_id) - 1
            if 0 <= idx < len(self.current_outline['sections']):
                section = self.current_outline['sections'][idx]
                
                print(f"🔄 Regenerujem sekciu: {section['title']}")
                
                # Regeneruj podsekcie s novými nápadmi
                topic = self.current_outline['topic']
                field = self.current_outline['field_code']
                
                new_subsections = self.planner.generate_topic_specific_subsections(
                    topic, section['id'], field
                )
                
                if new_subsections:
                    print(f"✨ Navrhované nové podsekcie:")
                    for i, sub in enumerate(new_subsections, 1):
                        print(f"  {i}. {sub}")
                    
                    if input("\n❓ Pridať tieto podsekcie? (y/n): ").lower() == 'y':
                        section['subsections'].extend(new_subsections)
                        section['estimated_pages'] = len(section['subsections']) * 2
                        print("✅ Podsekcie boli pridané!")
                else:
                    print("💡 Žiadne nové návrhy pre túto sekciu.")
                    
            else:
                print("❌ Neplatné číslo sekcie!")
        except ValueError:
            print("❌ Zadajte platné číslo!")
            
    def _save_and_continue(self):
        """Uloží finálnu osnovu a pripraví na písanie."""
        
        print("\n💾 UKLADÁM FINÁLNU OSNOVU...")
        
        # Ulož osnovu
        filename = self.planner.save_outline(self.current_outline)
        
        # Ulož aj JSON verziu pre ďalšie použitie
        json_filename = filename.replace('.md', '.json')
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.current_outline, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Osnova uložená: {filename}")
        print(f"📋 JSON verzia: {json_filename}")
        
        # Vytvor súbor s inštrukciami pre krok 2
        instructions = self._create_writing_instructions()
        instructions_file = f"WRITING_INSTRUCTIONS_{self.current_outline['topic'].replace(' ', '_')}.md"
        
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
            
        print(f"📝 Inštrukcie pre písanie: {instructions_file}")
        print()
        print("🎯 OSNOVA JE PRIPRAVENÁ!")
        print("➡️  Teraz môžete pokračovať na KROK 2: Písanie textu")
        print(f"🗂️ Použite súbor: {json_filename}")
        
    def _create_writing_instructions(self):
        """Vytvorí inštrukcie pre písanie na základe osnovy."""
        
        instructions = f"""# INŠTRUKCIE PRE PÍSANIE KAPITOLY

## 📋 ZÁKLADNÉ INFORMÁCIE
- **Téma:** {self.current_outline['topic']}
- **Odbor:** {self.current_outline['field']}
- **Cieľová dĺžka:** {self.current_outline['estimated_pages']} strán
- **Počet zdrojov:** {self.current_outline['estimated_sources']['total_recommended']}
- **JSON súbor osnovy:** {self.current_outline['topic'].replace(' ', '_')}.json

## 🎯 ŠTRUKTÚRA KAPITOLY

"""
        
        for section in self.current_outline['sections']:
            instructions += f"### {section['id']}. {section['title']}\n"
            instructions += f"*Cieľová dĺžka: ~{section.get('estimated_pages', 6)} strán*\n\n"
            
            for i, subsection in enumerate(section['subsections'], 1):
                instructions += f"{section['id']}.{i} {subsection}\n"
            
            instructions += f"\n**Kľúčové prvky:**\n"
            for element in section.get('key_elements', []):
                instructions += f"- {element}\n"
            instructions += "\n"
            
        instructions += f"""
## 📚 ODPORÚČANIA PRE ZDROJE
- Slovenské zdroje: {self.current_outline['estimated_sources']['slovak_sources']}
- Medzinárodné zdroje: {self.current_outline['estimated_sources']['international_sources']}
- Prirodzene zmiešať v texte (bez SK1, SK2 označení)
- Použiť aktuálne zdroje (2015-2024)

## ✍️ ŠTÝL PÍSANIA
- Akademický, ale zrozumiteľný
- Vyzerať ako práca vynikajúceho študenta
- Technické termíny vysvetliť
- Použiť konkrétne údaje a príklady
- Pridať obrázky/grafy kde je to vhodné

## 🔧 ĎALŠIE KROKY
1. Spustiť chapter_writer.py s týmto JSON súborom
2. Skontrolovať vygenerovaný text
3. Použiť humanizer pre finálne vylepšenia

---
*Vygenerované: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        
        return instructions

def main():
    """Hlavná funkcia pre interaktívnu tvorbu osnovy."""
    
    creator = InteractiveOutlineCreator()
    creator.start_interactive_session()

if __name__ == "__main__":
    main()