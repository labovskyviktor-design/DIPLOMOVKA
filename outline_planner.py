#!/usr/bin/env python3
"""
Inteligentný plánovač osnov pre akademické práce.
Analyzuje tému a vytvorí detailnú štruktúru kapitoly s obsahom a odporúčaniami.
"""

import re
import json
from datetime import datetime

class OutlinePlanner:
    """Inteligentný plánovač akademických osnov."""
    
    def __init__(self):
        """Inicializuje plánovač s databázou template-ov pre rôzne odbory."""
        
        # Template pre technické odbory
        self.technical_template = {
            "sections": [
                {"id": "1", "title": "Úvod a teoretické základy", "subsections": [
                    "Definícia problému a vymedzenie pojmov",
                    "Historický vývoj a súčasný stav",
                    "Ciele a hypotézy výskumu"
                ]},
                {"id": "2", "title": "Teoreticko-metodologické východiská", "subsections": [
                    "Teoretické koncepty a modely",
                    "Matematické a fyzikálne základy",
                    "Metodológia výskumu"
                ]},
                {"id": "3", "title": "Technologické riešenia a systémy", "subsections": [
                    "Súčasné technológie a nástroje", 
                    "Komparatívna analýza riešení",
                    "Inovatívne prístupy"
                ]},
                {"id": "4", "title": "Praktická aplikácia a výsledky", "subsections": [
                    "Implementácia a testing",
                    "Analýza výsledkov", 
                    "Ekonomické aspekty"
                ]},
                {"id": "5", "title": "Záver a perspektívy", "subsections": [
                    "Zhrnutie kľúčových zistení",
                    "Praktické odporúčania",
                    "Budúce smery výskumu"
                ]}
            ]
        }
        
        # Template pre pedagogické/humanitné odbory  
        self.pedagogical_template = {
            "sections": [
                {"id": "1", "title": "Úvod a vymedzenie problematiky", "subsections": [
                    "Definícia a kontextualizácia témy",
                    "Aktuálnosť a relevancia problému", 
                    "Ciele a výskumné otázky"
                ]},
                {"id": "2", "title": "Teoretické základy a literárny prehľad", "subsections": [
                    "Teoretické koncepty a teórie",
                    "Analýza súčasného stavu poznania",
                    "Medzery v výskume"
                ]},
                {"id": "3", "title": "Metodológia výskumu", "subsections": [
                    "Výskumný dizajn a prístup",
                    "Vzorka a zber dát",
                    "Nástroje a techniky analýzy"
                ]},
                {"id": "4", "title": "Výsledky a diskusia", "subsections": [
                    "Prezentácia výsledkov",
                    "Interpretácia a diskusia",
                    "Implikácie pre prax"
                ]},
                {"id": "5", "title": "Záver a odporúčania", "subsections": [
                    "Zhrnutie hlavných zistení",
                    "Odporúčania pre prax",
                    "Návrhy na ďalší výskum"
                ]}
            ]
        }
        
        # Template pre ekonomické/obchodné odbory
        self.economic_template = {
            "sections": [
                {"id": "1", "title": "Úvod a ekonomické prostredie", "subsections": [
                    "Ekonomický kontext a význam témy",
                    "Definícia problému a ciele",
                    "Štruktúra a metodika práce"
                ]},
                {"id": "2", "title": "Teoretické základy a literárny prehľad", "subsections": [
                    "Ekonomické teórie a koncepty",
                    "Analýza existujúcich štúdií", 
                    "Teoretický rámec výskumu"
                ]},
                {"id": "3", "title": "Analýza trhu a prostředia", "subsections": [
                    "Analýza makroekonomického prostredia",
                    "Sektorová analýza",
                    "SWOT analýza a competitive analysis"
                ]},
                {"id": "4", "title": "Empirická analýza a výsledky", "subsections": [
                    "Kvantitaívna analýza dát",
                    "Finančná analýza a projekcie",
                    "Vyhodnotenie hypotéz"
                ]},
                {"id": "5", "title": "Záver a business implikácie", "subsections": [
                    "Kľúčové ekonomické zistenia",
                    "Strategické odporúčania",
                    "Rizika a limitácie"
                ]}
            ]
        }

    def detect_field(self, topic: str) -> str:
        """Detekuje odbor na základe témy."""
        
        topic_lower = topic.lower()
        
        # Technické indikátory
        technical_keywords = [
            'systém', 'technológia', 'algoritmus', 'optimalizácia', 'model',
            'simulácia', 'analýza', 'implementácia', 'automatizácia', 'iot',
            'ai', 'strojové učenie', 'inžinierstvo', 'hydraulický', 'mechanický',
            'elektrotechnický', 'informatika', 'software', 'hardware'
        ]
        
        # Pedagogické indikátory
        pedagogical_keywords = [
            'vzdelávanie', 'výučba', 'učenie', 'študenti', 'žiaci', 'pedagógia', 
            'didaktika', 'metodika', 'kurikulum', 'škola', 'univerzita',
            'jazykové', 'literárne', 'kultúrne', 'sociálne', 'psychológia',
            'filozofia', 'história', 'umenie'
        ]
        
        # Ekonomické indikátory  
        economic_keywords = [
            'ekonomika', 'obchod', 'finance', 'marketing', 'management',
            'podnikanie', 'trh', 'investície', 'náklady', 'príjmy', 
            'stratégia', 'business', 'korporátne', 'financial'
        ]
        
        # Skórové hodnotenie
        tech_score = sum(1 for keyword in technical_keywords if keyword in topic_lower)
        ped_score = sum(1 for keyword in pedagogical_keywords if keyword in topic_lower)  
        eco_score = sum(1 for keyword in economic_keywords if keyword in topic_lower)
        
        if tech_score >= ped_score and tech_score >= eco_score:
            return "technical"
        elif ped_score >= eco_score:
            return "pedagogical"  
        else:
            return "economic"

    def generate_outline(self, topic: str, field_hint: str = None) -> dict:
        """Generuje detailnú osnovu pre danú tému."""
        
        print(f"🎯 Analyzujem tému: '{topic}'")
        
        # Detekuj odbor
        if field_hint:
            detected_field = field_hint
            print(f"🔧 Používam zadaný odbor: {detected_field}")
        else:
            detected_field = self.detect_field(topic)
            print(f"🔍 Detekovaný odbor: {detected_field}")
        
        # Vyber template
        if detected_field == "technical":
            template = self.technical_template
            field_name = "Technické/Inžinierske vedy"
        elif detected_field == "pedagogical":
            template = self.pedagogical_template  
            field_name = "Pedagogické/Humanitné vedy"
        else:
            template = self.economic_template
            field_name = "Ekonomické/Obchodné vedy"
        
        # Prispôsob template na konkrétnu tému
        customized_outline = self.customize_outline(topic, template, detected_field)
        
        # Pridaj metadata
        outline = {
            "topic": topic,
            "field": field_name,
            "field_code": detected_field,
            "generated_at": datetime.now().isoformat(),
            "estimated_pages": self.estimate_length(customized_outline),
            "estimated_sources": self.estimate_sources(customized_outline),
            "sections": customized_outline["sections"],
            "recommendations": self.generate_recommendations(topic, detected_field)
        }
        
        return outline

    def customize_outline(self, topic: str, template: dict, field: str) -> dict:
        """Prispôsobí template na konkrétnu tému."""
        
        customized = {"sections": []}
        
        for section in template["sections"]:
            # Prispôsob názov sekcie pre tému
            customized_title = self.adapt_section_title(section["title"], topic, field)
            
            # Prispôsob subsekcie
            customized_subsections = []
            for subsection in section["subsections"]:
                adapted = self.adapt_subsection_title(subsection, topic, field)
                customized_subsections.append(adapted)
            
            # Pridaj 1-2 špecifické subsekcie pre tému
            topic_specific = self.generate_topic_specific_subsections(topic, section["id"], field)
            customized_subsections.extend(topic_specific)
            
            customized["sections"].append({
                "id": section["id"],
                "title": customized_title,
                "subsections": customized_subsections,
                "estimated_pages": len(customized_subsections) * 2,
                "key_elements": self.suggest_key_elements(section["id"], topic, field)
            })
        
        return customized

    def adapt_section_title(self, title: str, topic: str, field: str) -> str:
        """Prispôsobí názov sekcie na konkrétnu tému."""
        
        # Získaj kľúčové slová z témy
        topic_words = topic.lower().split()
        main_concept = topic_words[0] if topic_words else "daná problematika"
        
        # Adaptácie pre rôzne sekcie
        adaptations = {
            "úvod": f"Úvod a vymedzenie problematiky {main_concept}",
            "teoretické": f"Teoretické základy {main_concept}",
            "technologické": f"Technologické riešenia v oblasti {main_concept}",
            "metodológia": f"Metodológia výskumu {main_concept}",
            "výsledky": f"Analýza výsledkov a zistení o {main_concept}",
            "záver": f"Záver a perspektívy rozvoja {main_concept}"
        }
        
        # Nájdi najlepšiu adaptáciu
        title_lower = title.lower()
        for key, adaptation in adaptations.items():
            if key in title_lower:
                return adaptation
        
        return title  # Ak žiadna adaptácia, vráť pôvodný

    def adapt_subsection_title(self, subsection: str, topic: str, field: str) -> str:
        """Prispôsobí názov podsekcie na tému."""
        
        # Jednoduchá adaptácia - pridaj kontext témy tam kde to dáva zmysel
        topic_context = topic.split()[0].lower() if topic else "danej oblasti"
        
        if "definícia" in subsection.lower():
            return f"Definícia a vymedzenie pojmov v oblasti {topic_context}"
        elif "analýza" in subsection.lower() and "súčasný" in subsection.lower():
            return f"Analýza súčasného stavu {topic_context}"
        elif "metodológia" in subsection.lower():
            return f"Metodológia výskumu v oblasti {topic_context}"
        
        return subsection

    def generate_topic_specific_subsections(self, topic: str, section_id: str, field: str) -> list:
        """Generuje špecifické podsekcie pre danú tému."""
        
        topic_lower = topic.lower()
        specific_subsections = []
        
        if field == "technical":
            if section_id == "2":  # Teoretické základy
                if any(word in topic_lower for word in ['hydraulický', 'tepelný', 'energetický']):
                    specific_subsections.append("Termodynamické aspekty a energetická efektívnosť")
                if any(word in topic_lower for word in ['systém', 'automatizácia', 'riadenie']):
                    specific_subsections.append("Systémová analýza a riadiace algoritmy")
            elif section_id == "3":  # Technológie
                specific_subsections.append("Moderné nástroje a softvérové riešenia")
                if "iot" in topic_lower or "inteligent" in topic_lower:
                    specific_subsections.append("IoT integrácia a smart technológie")
        
        elif field == "pedagogical":
            if section_id == "2":  # Teoretické základy  
                if "jazyk" in topic_lower or "výučba" in topic_lower:
                    specific_subsections.append("Teórie osvojovania si jazyka a didaktické prístupy")
                if "deti" in topic_lower or "primárn" in topic_lower:
                    specific_subsections.append("Vývojová psychológia a kognitívne aspekty")
            elif section_id == "4":  # Výsledky
                specific_subsections.append("Kvalitatívne a kvantitatívne výsledky výskumu")
        
        elif field == "economic":
            if section_id == "3":  # Analýza
                specific_subsections.append("Porter's Five Forces analýza")
                specific_subsections.append("Analýza stakeholderov a value chain")
            elif section_id == "4":  # Empirická analýza
                specific_subsections.append("Financial modeling a ROI analýza")
        
        return specific_subsections

    def suggest_key_elements(self, section_id: str, topic: str, field: str) -> list:
        """Navrhuje kľúčové prvky ktoré by sekcia mala obsahovať."""
        
        elements = {
            "1": [  # Úvod
                "Aktuálnosť a významnosť témy",
                "Jasne formulované ciele a hypotézy", 
                "Vymedzenie rozsahu a limitácií štúdie",
                "Štruktúra práce a metodický postup"
            ],
            "2": [  # Teoretické základy
                "Systematický prehľad literatúry",
                "Teoretické koncepty a definície",
                "Kritická analýza existujúcich prístupov", 
                "Identifikácia medzier vo výskume"
            ],
            "3": [  # Stredná časť (najvariabilnejšia)
                "Detailný popis metodológie/technológie",
                "Porovnávacie analýzy", 
                "Príkladové štúdie alebo case studies",
                "Validácia prístupov"
            ],
            "4": [  # Výsledky/Aplikácia
                "Prezentácia výsledkov s vizualizáciou",
                "Štatistická analýza a interpretácia",
                "Diskusia o praktických implikáciách",
                "Limitácie a reliability výsledkov"
            ],
            "5": [  # Záver
                "Zhrnutie kľúčových prínosov práce",
                "Odpovede na výskumné otázky", 
                "Praktické odporúčania",
                "Návrhy na ďalší výskum"
            ]
        }
        
        return elements.get(section_id, ["Relevantný obsah pre túto sekciu"])

    def estimate_length(self, outline: dict) -> int:
        """Odhaduje dĺžku práce v stranách."""
        
        base_pages = 0
        for section in outline["sections"]:
            # 2-4 strany na podsekciu v závislosti od komplexnosti
            subsection_pages = len(section["subsections"]) * 3
            base_pages += subsection_pages
        
        # Pridaj strany pre úvod, záver, bibliografiu, prílohy
        total_pages = base_pages + 15
        
        return min(max(total_pages, 25), 80)  # Rozumné limity 25-80 strán

    def estimate_sources(self, outline: dict) -> dict:
        """Odhaduje počet potrebných zdrojov."""
        
        total_sections = len(outline["sections"])
        
        return {
            "total_minimum": total_sections * 8,
            "total_recommended": total_sections * 12,
            "slovak_sources": "40-50%",
            "international_sources": "50-60%", 
            "books": "20-30%",
            "journal_articles": "50-60%",
            "conference_papers": "10-15%",
            "online_sources": "5-10%"
        }

    def generate_recommendations(self, topic: str, field: str) -> dict:
        """Generuje odporúčania pre výskum."""
        
        base_recommendations = {
            "research_approach": "Kombinovať kvalitatívny a kvantitatívny výskum",
            "sources": "Vyvážiť slovenské a medzinárodné zdroje (50:50)",
            "methodology": "Jasne opísať methodology a možné limitácie",
            "validation": "Validovať výsledky na reálnych dátach/prípadoch"
        }
        
        if field == "technical":
            base_recommendations.update({
                "prototyping": "Zvážiť vytvorenie prototypu alebo simulácie",
                "standards": "Referencovať relevantné technické štandardy", 
                "performance": "Definovať metriky výkonnosti a benchmarky"
            })
        elif field == "pedagogical":
            base_recommendations.update({
                "ethics": "Získať súhlas etickej komisie pre výskum s deťmi",
                "sample": "Zabezpečiť reprezentatívny výskumný vzorka",
                "instruments": "Validované výskumné nástroje a dotazníky"
            })
        elif field == "economic":
            base_recommendations.update({
                "data": "Používať aktuálne ekonomické dáta a trendy",
                "analysis": "Aplikovať relevantné ekonomické modely",
                "forecasting": "Zvážiť predikcie a scenario planning"
            })
        
        return base_recommendations

    def save_outline(self, outline: dict, filename: str = None) -> str:
        """Uloží osnovu do súboru."""
        
        if not filename:
            # Vytvor filename z témy
            topic_clean = re.sub(r'[^\w\s-]', '', outline['topic'])
            topic_clean = re.sub(r'[-\s]+', '_', topic_clean)
            filename = f"OSNOVA_{topic_clean.upper()}.md"
        
        # Vytvor markdown obsah
        md_content = self.format_as_markdown(outline)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return filename

    def format_as_markdown(self, outline: dict) -> str:
        """Formátuje osnovu ako markdown."""
        
        content = f"""# OSNOVA AKADEMICKEJ PRÁCE

## 📋 ZÁKLADNÉ INFORMÁCIE
- **Téma:** {outline['topic']}
- **Odbor:** {outline['field']}  
- **Dátum vytvorenia:** {outline['generated_at'][:10]}
- **Odhadovaná dĺžka:** {outline['estimated_pages']} strán
- **Odhadovaný počet zdrojov:** {outline['estimated_sources']['total_recommended']}

## 📚 ŠTRUKTÚRA PRÁCE

"""
        
        for section in outline['sections']:
            content += f"### {section['id']}. {section['title']}\n"
            content += f"*Odhadovaná dĺžka: {section.get('estimated_pages', 6)} strán*\n\n"
            
            for i, subsection in enumerate(section['subsections'], 1):
                content += f"{section['id']}.{i} {subsection}\n"
            
            content += f"\n**Kľúčové prvky:**\n"
            for element in section['key_elements']:
                content += f"- {element}\n"
            
            content += "\n---\n\n"
        
        content += f"""## 🎯 ODPORÚČANIA PRE VÝSKUM

"""
        
        for key, value in outline['recommendations'].items():
            content += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        
        content += f"""

## 📊 ODHADOVANÉ ZDROJE

- **Celkový počet zdrojov:** {outline['estimated_sources']['total_minimum']}-{outline['estimated_sources']['total_recommended']}
- **Slovenské zdroje:** {outline['estimated_sources']['slovak_sources']}  
- **Medzinárodné zdroje:** {outline['estimated_sources']['international_sources']}
- **Knihy:** {outline['estimated_sources']['books']}
- **Časopisecké články:** {outline['estimated_sources']['journal_articles']}
- **Konferencie:** {outline['estimated_sources']['conference_papers']}
- **Online zdroje:** {outline['estimated_sources']['online_sources']}

---

*Osnova vygenerovaná inteligentným plánovačom - thesis-ai-agent*
"""
        
        return content

def interactive_outline_planner():
    """Interaktívny interface pre plánovanie osnovy."""
    
    print("🎓 INTELIGENTNÝ PLÁNOVAČ OSNOV")
    print("=" * 50)
    
    # Získaj tému od užívateľa
    topic = input("\n📝 Zadajte tému vašej práce: ").strip()
    
    if not topic:
        print("❌ Téma nemôže byť prázdna!")
        return
    
    # Voliteľne špecifikuj odbor
    print("\n🔧 Chcete špecifikovať odbor? (voliteľné)")
    print("1. Technické/Inžinierske vedy")
    print("2. Pedagogické/Humanitné vedy") 
    print("3. Ekonomické/Obchodné vedy")
    print("4. Nechať detectovať automaticky")
    
    field_choice = input("\nVaša voľba (1-4, alebo stlačte Enter pre autodetekciu): ").strip()
    
    field_mapping = {
        "1": "technical",
        "2": "pedagogical", 
        "3": "economic"
    }
    
    field_hint = field_mapping.get(field_choice)
    
    # Vytvor osnovu
    planner = OutlinePlanner()
    outline = planner.generate_outline(topic, field_hint)
    
    # Zobraz result
    print(f"\n✅ OSNOVA VYTVORENÁ!")
    print(f"📊 Detekovaný odbor: {outline['field']}")
    print(f"📄 Odhadovaná dĺžka: {outline['estimated_pages']} strán")
    print(f"📚 Odporúčaný počet zdrojov: {outline['estimated_sources']['total_recommended']}")
    
    # Ulož do súboru
    filename = planner.save_outline(outline)
    print(f"💾 Osnova uložená do: {filename}")
    
    return filename

if __name__ == "__main__":
    interactive_outline_planner()