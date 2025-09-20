#!/usr/bin/env python3
"""
Test skript pre demonštráciu funkcie vyhľadávania akademických zdrojov.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.research_assistant import ResearchAssistant

class MockLLM:
    """Simulovaný LLM pre testovanie."""
    def generate_response(self, prompt):
        if "hydraulické vyregulovanie" in prompt.lower():
            return """
🔍 VÝSKUMNÝ PREHĽAD PRE HYDRAULICKÉ VYREGULOVANIE BYTOVÝCH DOMOV

1. **Základný prehľad témy:**
Hydraulické vyregulovanie je kľúčový proces optimalizácie vykurovacích systémov v bytových domoch. Zabezpečuje rovnomerné rozdelenie tepla a znižuje energetickú spotrebu.

2. **Kľúčové pojmy a koncepty:**
- Hydraulická rovnováha systému
- Termostatické ventily
- Diferenciálne tlakové regulátory  
- Balansné ventily
- Prietokové charakteristiky

3. **Hlavné oblasti výskumu:**
- Optimalizácia distribúcie tepla
- Smart regulačné systémy
- Energetická efektívnosť
- Diagnostika hydraulických problémov
- Prediktívna regulácia

4. **Možné výskumné otázky:**
- Ako ovplyvňuje hydraulické vyregulovanie celkovú energetickú efektívnosť?
- Aké sú najefektívnejšie metódy balancingu vo veľkých bytových komplexoch?
- Môže AI zlepšiť proces automatického vyregulovania?

5. **Doporučené zdroje:**
- Energy and Buildings Journal
- Building and Environment
- Applied Thermal Engineering
- ASHRAE Transactions
            """
        return "Obecná odpoveď na výskumnú otázku."

def test_hydraulic_balancing_search():
    """Test vyhľadávania pre hydraulické vyregulovanie."""
    print("🧪 TESTOVANIE AKADEMICKÉHO VYHĽADÁVANIA")
    print("=" * 50)
    
    # Vytvorenie mock LLM a research assistanta
    mock_llm = MockLLM()
    research_assistant = ResearchAssistant(mock_llm, {})
    
    # Test 1: Základný výskum témy
    print("\n📋 TEST 1: Základný výskum témy")
    print("-" * 30)
    topic = "hydraulické vyregulovanie bytových domov"
    result = research_assistant.research_topic(topic)
    print(result)
    
    # Test 2: Simulované vyhľadávanie zdrojov
    print("\n📋 TEST 2: Vyhľadávanie akademických zdrojov")  
    print("-" * 30)
    
    # Simulujeme vyhľadávanie s mock dátami
    mock_results = [
        {
            'title': 'Hydraulic Balancing of Heating Systems in Multi-Story Buildings',
            'authors': ['Novák, P.', 'Svoboda, J.'],
            'year': '2023',
            'journal': 'Energy and Buildings',
            'doi': '10.1016/j.enbuild.2023.112945',
            'abstract': 'This paper presents a comprehensive study on hydraulic balancing techniques for heating systems in residential buildings...',
            'source': 'Semantic Scholar'
        },
        {
            'title': 'Smart Control Systems for District Heating Distribution',
            'authors': ['Král, M.', 'Horáček, T.'],
            'year': '2022', 
            'journal': 'Applied Thermal Engineering',
            'doi': '10.1016/j.applthermaleng.2022.118567',
            'abstract': 'Implementácia inteligentných regulačných systémov pre distribúciu tepla...',
            'source': 'ArXiv'
        },
        {
            'title': 'Energetická efektívnosť bytových domov po hydraulickom vyregulaní',
            'authors': ['Baláž, A.', 'Kováč, L.'],
            'year': '2024',
            'journal': 'Stavebný obzor',
            'doi': 'N/A',
            'abstract': 'Analýza úspor energie v 15 bytových domoch po implementácii hydraulického vyregulovania...',
            'source': 'Google Scholar'
        }
    ]
    
    formatted_results = research_assistant._format_search_results(mock_results, topic)
    print(formatted_results)
    
    # Test 3: Test prekladu
    print("\n📋 TEST 3: Test prekladovej funkcie")
    print("-" * 30)
    
    english_text = "Hydraulic balancing ensures optimal heat distribution in heating systems"
    translation_result = research_assistant.translate_text(english_text, "sk")
    print(f"🔄 Preklad: {translation_result}")
    
    slovak_text = "Hydraulické vyregulovanie zabezpečuje optimálne rozdelenie tepla"
    translation_result2 = research_assistant.translate_text(slovak_text, "en") 
    print(f"🔄 Preklad: {translation_result2}")

    # Test 4: Generovanie manuálnych návrhov zdrojov
    print("\n📋 TEST 4: Manuálne návrhy zdrojov")
    print("-" * 30)
    
    manual_suggestions = research_assistant._generate_manual_source_suggestions(topic)
    print(manual_suggestions)

if __name__ == "__main__":
    test_hydraulic_balancing_search()