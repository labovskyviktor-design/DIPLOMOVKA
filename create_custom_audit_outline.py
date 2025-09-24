#!/usr/bin/env python3
"""
Vytvorenie upravenej osnovy pre energetický audit s kapitolou "Návrh opatrení"
so špecializáciou na hydraulické vyregulovanie.
"""

import json
from datetime import datetime

def create_custom_audit_outline():
    """Vytvorí upravenú osnovu s kapitolou Návrh opatrení."""
    
    outline = {
        "topic": "Energetický audit a hydraulické vyregulovanie",
        "field": "Technické/Inžinierske vedy",
        "field_code": "technical",
        "generated_at": datetime.now().isoformat(),
        "estimated_pages": 65,
        "estimated_sources": {
            "total_minimum": 60,
            "total_recommended": 75,
            "slovak_sources": "45-50%",
            "international_sources": "50-55%",
            "books": "20-30%",
            "journal_articles": "50-60%",
            "conference_papers": "10-15%",
            "online_sources": "5-10%"
        },
        "sections": [
            {
                "id": "1",
                "title": "Úvod a vymedzenie problematiky energetického auditu",
                "subsections": [
                    "Definícia energetického auditu a hydraulického vyregulovania",
                    "Legislatívny rámec a normy v SR a EÚ",
                    "Aktuálnosť a význam energetických auditov",
                    "Ciele a hypotézy výskumu"
                ],
                "estimated_pages": 8,
                "key_elements": [
                    "Jasné definície základných pojmov",
                    "Prejavy z legislatívy SR (zákon o energetickej efektívnosti)",
                    "Európske smernice o energetickej efektívnosti budov",
                    "Štatistiky energetických úspor v SR"
                ]
            },
            {
                "id": "2", 
                "title": "Teoretické základy energetickej efektívnosti",
                "subsections": [
                    "Termodynamické základy tepelných strát",
                    "Hydraulické princípy distribúcie tepla",
                    "Metodológia energetického auditu",
                    "Meranie a monitorovanie energetických parametrov"
                ],
                "estimated_pages": 10,
                "key_elements": [
                    "Základné rovnice tepelných strát",
                    "Hydraulické výpočty prietokov a tlakov",
                    "Metodiky EN 16247 pre energetické audity",
                    "Meracie prístroje a ich presnosť"
                ]
            },
            {
                "id": "3",
                "title": "Energetický audit budovy - praktická realizácia", 
                "subsections": [
                    "Prípravná fáza auditu a zber podkladov",
                    "Obhliadka budovy a zisťovanie skutočného stavu",
                    "Meranie spotreby energií a parametrov prostredia",
                    "Identifikácia energetických nedostatkov"
                ],
                "estimated_pages": 12,
                "key_elements": [
                    "Checklist pre energetický audit", 
                    "Termografické snímkovanie obálky budovy",
                    "Meranie účinnosti vykurovacieho systému",
                    "Analýza spotrebných charakteristík"
                ]
            },
            {
                "id": "4",
                "title": "Návrh opatrení na zvýšenie energetickej efektívnosti",
                "subsections": [
                    "Hydraulické vyregulovanie vykurovacích systémov",
                    "Optimalizácia prevádzky tepelných zdrojov",
                    "Izolačné opatrenia na obálke budovy", 
                    "Modernizácia rozvodov tepla a regulácie",
                    "Implementácia obnoviteľných zdrojov energie",
                    "Automatizácia a inteligentné riadenie systémov"
                ],
                "estimated_pages": 18,
                "key_elements": [
                    "Postup hydraulického vyregulovania krok za krokom",
                    "Výpočet regulačných ventilov a ich nastavenie",
                    "Vyváženie prietokov v jednotlivých okruhoch",
                    "ROI analýza jednotlivých opatrení",
                    "Kombinácia opatrení pre maximálnu efektívnosť",
                    "Implementačný plán a harmonogram"
                ]
            },
            {
                "id": "5",
                "title": "Case study - komplexný energetický audit",
                "subsections": [
                    "Charakteristika riešeného objektu",
                    "Realizácia energetického auditu",
                    "Návrh komplexného riešenia s hydraulickým vyregulovaním",
                    "Ekonomické vyhodnotenie a návratnosť investície",
                    "Implementácia opatrení a monitoring úspor"
                ],
                "estimated_pages": 12,
                "key_elements": [
                    "Reálny projekt s konkrétnymi údajmi",
                    "Merania pred a po implementácii opatrení",
                    "Detailný rozpočet investičných nákladov",
                    "Overenie dosiahnutých úspor v praxi"
                ]
            },
            {
                "id": "6", 
                "title": "Záver a odporúčania",
                "subsections": [
                    "Zhrnutie kľúčových poznatkov",
                    "Overenie hypotéz a dosiahnutie cieľov",
                    "Odporúčania pre prax energetických auditov",
                    "Budúce trendy v oblasti energetickej efektívnosti"
                ],
                "estimated_pages": 5,
                "key_elements": [
                    "Kvantitatívne zhodnotenie prínosov práce",
                    "Metodické odporúčania pre audítorov",
                    "Identifikácia oblastí pre ďalší výskum",
                    "Perspektívy digitalizácie energetických auditov"
                ]
            }
        ],
        "recommendations": {
            "research_approach": "Kombinovať teoretickú analýzu s praktickou realizáciou",
            "sources": "Vyvážiť slovenské normy a prax s medzinárodnými štandardmi (50:50)",
            "methodology": "Použiť reálny case study pre overenie teoretických poznatkov",
            "validation": "Validovať výsledky meraním pred a po implementácii opatrení",
            "prototyping": "Vytvoriť kompletnú metodiku hydraulického vyregulovania",
            "standards": "Referencovať STN EN 15316, STN EN 16247 a ďalšie relevantné normy",
            "performance": "Definovať KPI pre hodnotenie úspešnosti energetických opatrení",
            "case_study": "Použiť reálny objekt pre praktické overenie návrhov"
        }
    }
    
    return outline

def save_custom_outline():
    """Uloží upravenú osnovu do súborov."""
    
    outline = create_custom_audit_outline()
    
    # Ulož JSON verziu
    json_filename = "OSNOVA_ENERGETICKY_AUDIT_UPRAVENA.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)
    
    # Vytvor Markdown verziu
    md_content = format_as_markdown(outline)
    md_filename = "OSNOVA_ENERGETICKY_AUDIT_UPRAVENA.md"
    
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print("✅ UPRAVENÁ OSNOVA VYTVORENÁ!")
    print("=" * 50)
    print(f"📋 JSON súbor: {json_filename}")
    print(f"📄 Markdown súbor: {md_filename}")
    print()
    
    # Zobraz prehľad
    print("📚 PREHĽAD KAPITOL:")
    for section in outline['sections']:
        print(f"{section['id']}. {section['title']} (~{section['estimated_pages']} strán)")
        
        # Zobraz podsekcie pre kapitolu 4 (Návrh opatrení)
        if section['id'] == '4':
            print("   🔧 Kľúčové podsekcie:")
            for subsection in section['subsections']:
                print(f"      • {subsection}")
    
    print(f"\n📊 Celková dĺžka: {outline['estimated_pages']} strán")
    print(f"📚 Počet zdrojov: {outline['estimated_sources']['total_recommended']}")
    
    return json_filename

def format_as_markdown(outline):
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
        content += f"*Odhadovaná dĺžka: {section['estimated_pages']} strán*\n\n"
        
        for i, subsection in enumerate(section['subsections'], 1):
            content += f"{section['id']}.{i} {subsection}\n"
        
        content += f"\n**Kľúčové prvky:**\n"
        for element in section['key_elements']:
            content += f"- {element}\n"
        
        content += "\n---\n\n"
    
    content += f"""## 🎯 ODPORÚČANIA PRE VÝSKUM

"""
    
    for key, value in outline['recommendations'].items():
        key_formatted = key.replace('_', ' ').title()
        content += f"- **{key_formatted}:** {value}\n"
    
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

*Osnova upravená pre špecializáciu na hydraulické vyregulovanie - thesis-ai-agent*
"""
    
    return content

if __name__ == "__main__":
    save_custom_outline()