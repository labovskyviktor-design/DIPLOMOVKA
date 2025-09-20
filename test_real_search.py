#!/usr/bin/env python3
"""
Test skutočného API vyhľadávania v Semantic Scholar pre hydraulické vyregulovanie.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.research_assistant import ResearchAssistant
import requests

class MockLLM:
    """Simulovaný LLM pre testovanie."""
    def generate_response(self, prompt):
        return "Mock LLM response for testing purposes."

def test_real_semantic_scholar_search():
    """Test skutočného vyhľadávania v Semantic Scholar."""
    print("🔍 TEST SKUTOČNÉHO VYHĽADÁVANIA - SEMANTIC SCHOLAR")
    print("=" * 60)
    
    research_assistant = ResearchAssistant(MockLLM(), {})
    
    # Test 1: Vyhľadávanie anglických výrazov
    print("\n📋 TEST 1: Vyhľadávanie - 'hydraulic balancing heating systems'")
    print("-" * 50)
    
    query = "hydraulic balancing heating systems"
    results = research_assistant._search_semantic_scholar(query, 3)
    
    if results:
        formatted = research_assistant._format_search_results(results, query)
        print(formatted)
    else:
        print("❌ Žiadne výsledky z Semantic Scholar API")
    
    # Test 2: Vyhľadávanie pre building heating
    print("\n📋 TEST 2: Vyhľadávanie - 'building heating distribution'")
    print("-" * 50)
    
    query2 = "building heating distribution"
    results2 = research_assistant._search_semantic_scholar(query2, 3)
    
    if results2:
        formatted2 = research_assistant._format_search_results(results2, query2)
        print(formatted2)
    else:
        print("❌ Žiadne výsledky z Semantic Scholar API")
    
    # Test 3: Manuálne testovanie Semantic Scholar API priamo
    print("\n📋 TEST 3: Priame testovanie Semantic Scholar API")
    print("-" * 50)
    
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            'query': 'hydraulic balancing heating systems',
            'limit': 3,
            'fields': 'title,authors,year,abstract,journal'
        }
        
        print(f"🔗 URL: {url}")
        print(f"📊 Parametre: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📈 Počet výsledkov: {len(data.get('data', []))}")
            
            for i, paper in enumerate(data.get('data', []), 1):
                print(f"\n[{i}] {paper.get('title', 'N/A')}")
                authors = [author.get('name', 'N/A') for author in paper.get('authors', [])]
                print(f"   Autori: {', '.join(authors)}")
                print(f"   Rok: {paper.get('year', 'N/A')}")
                if paper.get('journal'):
                    print(f"   Časopis: {paper.get('journal', {}).get('name', 'N/A')}")
                if paper.get('abstract'):
                    abstract_short = paper.get('abstract', '')[:100] + '...' if len(paper.get('abstract', '')) > 100 else paper.get('abstract', '')
                    print(f"   Abstrakt: {abstract_short}")
        else:
            print(f"❌ API chyba: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Chyba pri volaní API: {e}")

def test_translation_detection():
    """Test detekcie jazyka a prekladu."""
    print("\n🌐 TEST DETEKCIE JAZYKA A PREKLADU")
    print("=" * 40)
    
    research_assistant = ResearchAssistant(MockLLM(), {})
    
    # Test detekcie jazyka
    slovak_text = "hydraulické vyregulovanie bytových domov"
    english_text = "hydraulic balancing heating systems"
    mixed_text = "smart heating control systémy"
    
    print(f"Slovenský text: '{slovak_text}' -> {research_assistant._detect_language(slovak_text)}")
    print(f"Anglický text: '{english_text}' -> {research_assistant._detect_language(english_text)}")
    print(f"Zmiešaný text: '{mixed_text}' -> {research_assistant._detect_language(mixed_text)}")

if __name__ == "__main__":
    test_real_semantic_scholar_search()
    test_translation_detection()