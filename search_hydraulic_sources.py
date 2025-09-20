#!/usr/bin/env python3
"""
Komplexné vyhľadávanie akademických zdrojov pre hydraulické vyregulovanie bytových domov.
"""

import sys
import os
import requests
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.research_assistant import ResearchAssistant

class MockLLM:
    """Simulovaný LLM pre testovanie."""
    def generate_response(self, prompt):
        return "Mock response for demonstration"

def search_semantic_scholar_comprehensive():
    """Rozsiahle vyhľadávanie v Semantic Scholar."""
    print("🔍 SEMANTIC SCHOLAR - KOMPLEXNÉ VYHĽADÁVANIE")
    print("=" * 60)
    
    search_terms = [
        "hydraulic balancing heating systems",
        "district heating hydraulic balance",
        "building heating distribution optimization",
        "thermal comfort hydraulic systems",
        "energy efficiency heating networks",
        "heating system flow control",
        "radiator balancing residential buildings"
    ]
    
    all_results = []
    
    for i, term in enumerate(search_terms, 1):
        print(f"\n📋 VYHĽADÁVANIE {i}/{len(search_terms)}: '{term}'")
        print("-" * 50)
        
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                'query': term,
                'limit': 5,
                'fields': 'title,authors,year,abstract,journal'
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                papers = data.get('data', [])
                print(f"✅ Nájdené: {len(papers)} článkov")
                
                for j, paper in enumerate(papers, 1):
                    title = paper.get('title', 'N/A')
                    authors = [author.get('name', 'N/A') for author in paper.get('authors', [])]
                    year = paper.get('year', 'N/A')
                    journal = paper.get('journal', {}).get('name', 'N/A') if paper.get('journal') else 'N/A'
                    abstract = paper.get('abstract', 'N/A')
                    
                    print(f"\n  [{j}] {title}")
                    print(f"      Autori: {', '.join(authors[:3])}")  # Limit na 3 autorov
                    print(f"      Rok: {year}")
                    print(f"      Časopis: {journal}")
                    if abstract and abstract != 'N/A' and len(abstract) > 50:
                        print(f"      Abstrakt: {abstract[:150]}...")
                    
                    # Pridanie do kompletných výsledkov
                    all_results.append({
                        'title': title,
                        'authors': authors,
                        'year': year,
                        'journal': journal,
                        'abstract': abstract,
                        'search_term': term,
                        'source': 'Semantic Scholar'
                    })
                        
            else:
                print(f"❌ API Error: {response.status_code}")
                
            # Krátka pauza medzi requestami
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Chyba: {e}")
    
    return all_results

def search_arxiv_heating():
    """Vyhľadávanie v ArXiv pre technické témy."""
    print(f"\n🔍 ARXIV - TECHNICKÉ ČLÁNKY")
    print("=" * 60)
    
    search_terms = [
        "heating systems optimization",
        "building energy efficiency",
        "thermal systems control",
        "smart heating networks"
    ]
    
    # ArXiv má špecifické kategórie pre engineering
    categories = ['physics.app-ph', 'cs.SY', 'eess.SY']  # Applied physics, Systems and Control
    
    results = []
    
    for term in search_terms:
        print(f"\n📋 ArXiv vyhľadávanie: '{term}'")
        try:
            # ArXiv API endpoint
            base_url = "http://export.arxiv.org/api/query"
            query = f"all:{term}"
            url = f"{base_url}?search_query={query}&start=0&max_results=3"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Jednoduché parsovanie XML (pre demonštráciu)
                content = response.text
                if 'entry' in content:
                    print("✅ Nájdené články v ArXiv")
                    # V plnej implementácii by sme použili XML parser
                    results.append({
                        'search_term': term,
                        'status': 'found',
                        'source': 'ArXiv'
                    })
                else:
                    print("❌ Žiadne výsledky")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ ArXiv chyba: {e}")
    
    return results

def generate_manual_expert_sources():
    """Generuje manuálny zoznam expertných zdrojov a inštitúcií."""
    print(f"\n📚 EXPERTNÉ ZDROJE A INŠTITÚCIE")
    print("=" * 60)
    
    sources = {
        "📖 Kľúčové časopisy": [
            "Energy and Buildings (Elsevier)",
            "Applied Energy (Elsevier)", 
            "Building and Environment (Elsevier)",
            "Energy Efficiency (Springer)",
            "Journal of Building Engineering (Elsevier)",
            "International Journal of Thermal Sciences",
            "ASHRAE Transactions",
            "Building Services Engineering Research and Technology"
        ],
        
        "🏛️ Výskumné inštitúcie": [
            "International Energy Agency (IEA)",
            "European Centre for Building Energy Efficiency",
            "ASHRAE (American Society of HVAC Engineers)",
            "REHVA (Federation of European HVAC Associations)",
            "Technical University of Denmark (DTU) - Building Energy",
            "KTH Royal Institute of Technology - Energy Technology",
            "Fraunhofer Institute for Building Physics (IBP)"
        ],
        
        "👨‍🎓 Kľúčoví experti v oblasti": [
            "Stanislav Chicherin (Ural Federal University)",
            "Henrik Lund (Aalborg University)",
            "Svend Svendsen (Technical University of Denmark)",
            "Jan Eric Thorsen (Danfoss)",
            "Håkan Eriksson (KTH Stockholm)"
        ],
        
        "🔍 Kľúčové slová pre vyhľadávanie": [
            "hydraulic balancing",
            "district heating optimization", 
            "building heating distribution",
            "thermal comfort control",
            "heating system efficiency",
            "flow balancing valves",
            "pressure differential control",
            "smart heating networks"
        ],
        
        "📊 Konferencie a podujatia": [
            "International Conference on Energy Efficiency in Buildings",
            "ASHRAE Winter/Summer Conferences",
            "REHVA Annual Conferences", 
            "International Symposium on District Heating and Cooling",
            "Building Simulation Conference",
            "European Conference on Energy Efficiency"
        ]
    }
    
    for category, items in sources.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")
    
    return sources

def search_specific_heating_topics():
    """Vyhľadávanie špecifických tém hydraulického vyregulovania."""
    print(f"\n🎯 ŠPECIFICKÉ TÉMY HYDRAULICKÉHO VYREGULOVANIA")
    print("=" * 60)
    
    specific_queries = [
        "thermostatic radiator valves efficiency",
        "pressure independent control valves",
        "differential pressure controllers heating",
        "automated balancing systems",
        "heating network diagnostics"
    ]
    
    results = []
    research_assistant = ResearchAssistant(MockLLM(), {})
    
    for query in specific_queries:
        print(f"\n🔍 Špecifické vyhľadávanie: '{query}'")
        print("-" * 40)
        
        try:
            # Vyhľadávanie cez náš systém
            semantic_results = research_assistant._search_semantic_scholar(query, 3)
            
            if semantic_results:
                print(f"✅ Nájdené: {len(semantic_results)} zdrojov")
                for i, result in enumerate(semantic_results, 1):
                    print(f"  [{i}] {result['title']}")
                    print(f"      {', '.join(result['authors'][:2])} ({result['year']})")
                
                results.extend(semantic_results)
            else:
                print("❌ Žiadne výsledky")
                
        except Exception as e:
            print(f"❌ Chyba: {e}")
    
    return results

def generate_stn_citations(results):
    """Generuje citácie v STN ISO 690 formáte."""
    print(f"\n📖 STN ISO 690 CITÁCIE")
    print("=" * 60)
    
    print("Bibliografické citácie vo formáte STN ISO 690:")
    print()
    
    citation_count = 1
    seen_titles = set()  # Aby sme sa vyhli duplikátom
    
    for result in results:
        title = result.get('title', 'N/A')
        
        # Kontrola duplikátov
        if title in seen_titles or title == 'N/A':
            continue
        seen_titles.add(title)
        
        authors = result.get('authors', [])
        year = result.get('year', 'N/A')
        journal = result.get('journal', 'N/A')
        
        # Formátovanie autorov pre STN ISO 690
        if authors and len(authors) > 0:
            if len(authors) == 1:
                author_str = authors[0].upper()
            elif len(authors) <= 3:
                author_str = ', '.join([name.upper() for name in authors])
            else:
                author_str = f"{authors[0].upper()} et al."
        else:
            author_str = "AUTOR, N."
        
        # STN ISO 690 formát
        if journal and journal != 'N/A':
            citation = f"[{citation_count}] {author_str} {title}. In {journal}. {year}."
        else:
            citation = f"[{citation_count}] {author_str} {title}. {year}."
        
        print(citation)
        print()
        citation_count += 1
        
        if citation_count > 15:  # Limit na 15 citácií
            break

def main_comprehensive_search():
    """Hlavná funkcia pre komplexné vyhľadávanie."""
    print("🏠 KOMPLEXNÉ VYHĽADÁVANIE AKADEMICKÝCH ZDROJOV")
    print("Téma: Hydraulické vyregulovanie bytových domov")
    print("=" * 80)
    
    all_results = []
    
    # 1. Semantic Scholar vyhľadávanie
    semantic_results = search_semantic_scholar_comprehensive()
    all_results.extend(semantic_results)
    
    # 2. ArXiv vyhľadávanie
    arxiv_results = search_arxiv_heating()
    
    # 3. Špecifické témy
    specific_results = search_specific_heating_topics()
    all_results.extend(specific_results)
    
    # 4. Expertné zdroje
    expert_sources = generate_manual_expert_sources()
    
    # 5. Generovanie citácií
    if all_results:
        generate_stn_citations(all_results)
    
    # Súhrn
    print(f"\n📊 SÚHRN VYHĽADÁVANIA")
    print("=" * 60)
    print(f"✅ Celkový počet nájdených zdrojov: {len(all_results)}")
    print(f"📚 Databázy prehľadané: Semantic Scholar, ArXiv")
    print(f"🎯 Špecifické témy: 5 kategórií")
    print(f"👨‍🎓 Expertné zdroje: Časopisy, inštitúcie, konferencie")
    print()
    print("💡 Pre každý zdroj môžete použiť:")
    print("   • translate [abstrakt] - preklad abstraktu")
    print("   • cite [informácie] - vytvorenie citácie")

if __name__ == "__main__":
    main_comprehensive_search()