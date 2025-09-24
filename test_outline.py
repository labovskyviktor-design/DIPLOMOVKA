#!/usr/bin/env python3
"""
Test script pre vytvorenie osnovy na tému energetický audit a hydraulické vyregulovanie
"""

from outline_planner import OutlinePlanner
import json

def test_energy_audit_outline():
    """Test vytvorenia osnovy pre energetický audit."""
    
    # Vytvor planner
    planner = OutlinePlanner()
    
    # Vygeneruj osnovu
    topic = "Energetický audit a hydraulické vyregulovanie"
    outline = planner.generate_outline(topic, "technical")
    
    print("🎯 OSNOVA PRE:", topic.upper())
    print("=" * 60)
    print(f"📊 Odbor: {outline['field']}")
    print(f"📄 Odhadovaná dĺžka: {outline['estimated_pages']} strán")
    print(f"📚 Zdroje: {outline['estimated_sources']['total_recommended']}")
    print()
    
    # Zobraz štruktúru s očíslovaním 1-10
    print("📋 10-BODOVÁ OSNOVA:")
    print("-" * 30)
    
    counter = 1
    for section in outline['sections']:
        if counter <= 10:
            print(f"{counter}. {section['title']}")
            print(f"   📄 ~{section.get('estimated_pages', 6)} strán")
            counter += 1
            
            for subsection in section['subsections']:
                if counter <= 10:
                    print(f"{counter}. {subsection}")
                    counter += 1
                else:
                    break
        else:
            break
    
    print()
    print("🔧 KĽÚČOVÉ PRVKY OSNOVY:")
    print("-" * 25)
    
    for i, section in enumerate(outline['sections'][:3], 1):  # Prvé 3 sekcie
        print(f"\n📁 Sekcia {i}: {section['title']}")
        key_elements = section.get('key_elements', [])
        for element in key_elements[:3]:  # Prvé 3 elementy
            print(f"   • {element}")
    
    # Ulož detailnú osnovu
    print("\n💾 Ukladám detailnú osnovu...")
    filename = planner.save_outline(outline)
    print(f"✅ Uložené: {filename}")
    
    return outline

if __name__ == "__main__":
    test_energy_audit_outline()