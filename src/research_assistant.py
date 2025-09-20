"""
Výskumný asistent pre vyhľadávanie a analýzu zdrojov.
"""

import logging
import requests
import json
import re
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus


class ResearchAssistant:
    """Asistent pre výskumnú činnosť a literatúru."""
    
    def __init__(self, llm_interface, config: Dict[str, Any] = None):
        """
        Inicializácia výskumného asistenta.
        
        Args:
            llm_interface: Rozhranie pre jazykový model
            config: Konfigurácia pre vyhľadávanie a preklad
        """
        self.llm = llm_interface
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        self.translation_cache = {}  # Cache pre preklady
        
    def handle_research_query(self, command: str) -> str:
        """
        Spracuje výskumný dotaz.
        
        Args:
            command: Príkaz od používateľa
            
        Returns:
            Výskumná odpoveď
        """
        command_lower = command.lower()
        
        if "search" in command_lower or "hľadaj" in command_lower:
            topic = self._extract_topic(command)
            return self.search_academic_sources(topic)
        elif "translate" in command_lower or "preloži" in command_lower:
            text = self._extract_text_for_translation(command)
            return self.translate_text(text)
        elif "outline" in command_lower:
            topic = self._extract_topic(command)
            return self.generate_research_outline(topic)
        elif command_lower.startswith("research"):
            topic = self._extract_topic(command)
            return self.research_topic(topic)
        else:
            return self.llm.generate_response(f"Výskumný dotaz: {command}")
    
    def research_topic(self, topic: str) -> str:
        """
        Vykoná základný výskum témy.
        
        Args:
            topic: Výskumná téma
            
        Returns:
            Výsledky výskumu
        """
        prompt = f"""
        Ako výskumný asistent ti pomôžem s témou: "{topic}"

        Prosím poskytni:
        1. Základný prehľad témy
        2. Kľúčové pojmy a koncepty
        3. Hlavné oblasti výskumu
        4. Možné výskumné otázky
        5. Doporučené zdroje (typy publikácií, databázy)

        Odpoveď formátuj jasne a štruktúrovane.
        """
        
        return self.llm.generate_response(prompt)
    
    def generate_research_outline(self, topic: str) -> str:
        """
        Vytvorí výskumný obrys pre danú tému.
        
        Args:
            topic: Téma pre outline
            
        Returns:
            Štruktúrovaný outline
        """
        prompt = f"""
        Vytvor detailný výskumný outline pre tému: "{topic}"

        Outline by mal obsahovať:
        1. Úvod a kontext
        2. Teoretický rámec
        3. Literatúra a súčasný stav poznania
        4. Výskumné otázky/hypotézy
        5. Metodológia
        6. Očakávané výsledky
        7. Záver a implikácie

        Pre každú sekciu uveď 2-3 hlavné body a podpunkty.
        """
        
        return self.llm.generate_response(prompt)
    
    def suggest_sources(self, topic: str, source_type: str = "academic") -> str:
        """
        Navrhne relevantné zdroje pre výskum.
        
        Args:
            topic: Výskumná téma
            source_type: Typ zdrojov (academic, books, articles)
            
        Returns:
            Zoznam navrhnutých zdrojov
        """
        prompt = f"""
        Pre výskumnú tému "{topic}" navrhni relevantné zdroje typu "{source_type}".
        
        Uveď:
        1. Konkrétne názvy kníh/článkov (ak sú známe)
        2. Mená významných autorov v oblasti
        3. Relevantné vedecké časopisy
        4. Odporúčané databázy pre vyhľadávanie
        5. Kľúčové slová pre vyhľadávanie
        """
        
        return self.llm.generate_response(prompt)
    
    def analyze_gap(self, topic: str, current_knowledge: str) -> str:
        """
        Analyzuje medzery v súčasnom poznaní.
        
        Args:
            topic: Výskumná téma
            current_knowledge: Súčasné poznatky
            
        Returns:
            Analýza medzier a návrhov
        """
        prompt = f"""
        Téma výskumu: {topic}
        Súčasné poznatky: {current_knowledge}
        
        Analyzuj:
        1. Aké sú hlavné medzery v súčasnom poznaní?
        2. Aké nové výskumné smery by boli prínosné?
        3. Aké metodológie by mohli priniesť nové poznatky?
        4. Aké sú praktické aplikácie výskumu?
        """
        
        return self.llm.generate_response(prompt)
    
    def search_academic_sources(self, topic: str, max_results: int = 10) -> str:
        """
        Vyhľadá akademické zdroje pre danú tému.
        
        Args:
            topic: Téma pre vyhľadávanie
            max_results: Maximálny počet výsledkov
            
        Returns:
            Zoznam nájdených zdrojov
        """
        self.logger.info(f"Vyhľadávanie zdrojov pre tému: {topic}")
        
        results = []
        
        # Google Scholar search
        scholar_results = self._search_google_scholar(topic, max_results//2)
        if scholar_results:
            results.extend(scholar_results)
        
        # ArXiv search (pre technické témy)
        if any(keyword in topic.lower() for keyword in ['vykurovanie', 'heating', 'energy', 'thermal', 'building']):
            arxiv_results = self._search_arxiv(topic, max_results//4)
            if arxiv_results:
                results.extend(arxiv_results)
        
        # Semantic Scholar search
        semantic_results = self._search_semantic_scholar(topic, max_results//4)
        if semantic_results:
            results.extend(semantic_results)
        
        if not results:
            return self._generate_manual_source_suggestions(topic)
        
        return self._format_search_results(results, topic)
    
    def translate_text(self, text: str, target_lang: str = "sk") -> str:
        """
        Preloží text medzi slovenčinou a angličtinou.
        
        Args:
            text: Text na preklad
            target_lang: Cieľový jazyk (sk/en)
            
        Returns:
            Preložený text
        """
        if not text or len(text.strip()) < 3:
            return "❌ Zadajte text na preklad."
        
        # Kontrola cache
        cache_key = f"{text}_{target_lang}"
        if cache_key in self.translation_cache:
            return f"📝 Preklad (z cache): {self.translation_cache[cache_key]}"
        
        # Detekcia jazyka
        source_lang = self._detect_language(text)
        if source_lang == target_lang:
            return f"⚠️ Text je už v cieľovom jazyku ({target_lang})"
        
        # Pokús o preklad cez API
        translation = self._translate_via_api(text, source_lang, target_lang)
        
        if translation:
            self.translation_cache[cache_key] = translation
            return f"📝 Preklad ({source_lang} → {target_lang}): {translation}"
        else:
            # Fallback na LLM preklad
            return self._translate_via_llm(text, source_lang, target_lang)
    
    def _search_google_scholar(self, query: str, max_results: int) -> List[Dict]:
        """Vyhľadá v Google Scholar (simulované)."""
        # Poznámka: Google Scholar nemá oficiálne API, takže toto je simulácia
        # V reálnej implementácii by sme použili scholarly alebo serpapi
        try:
            # Simulujeme výsledky pre vykurovanie budov
            if 'vykurovanie' in query.lower() or 'heating' in query.lower():
                return [
                    {
                        'title': 'Energy Efficiency in Building Heating Systems: A Comprehensive Review',
                        'authors': ['Smith, J.', 'Johnson, M.'],
                        'year': '2023',
                        'journal': 'Energy and Buildings',
                        'doi': '10.1016/j.enbuild.2023.112845',
                        'abstract': 'This paper reviews modern heating technologies...',
                        'source': 'Google Scholar'
                    },
                    {
                        'title': 'Smart Heating Control Systems for Residential Buildings',
                        'authors': ['Wilson, K.', 'Brown, L.'],
                        'year': '2022',
                        'journal': 'Applied Energy',
                        'doi': '10.1016/j.apenergy.2022.119234',
                        'abstract': 'Smart control systems can significantly improve...',
                        'source': 'Google Scholar'
                    }
                ]
        except Exception as e:
            self.logger.error(f"Chyba pri vyhľadávaní Google Scholar: {e}")
        return []
    
    def _search_arxiv(self, query: str, max_results: int) -> List[Dict]:
        """Vyhľadá v ArXiv databáze."""
        try:
            # ArXiv API endpoint
            base_url = "http://export.arxiv.org/api/query"
            search_query = quote_plus(f"all:{query}")
            url = f"{base_url}?search_query={search_query}&start=0&max_results={max_results}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Parsovanie XML odpovede (zjednodušené)
                # V reálnej implementácii by sme použili xml.etree.ElementTree
                return self._parse_arxiv_response(response.text)
        except Exception as e:
            self.logger.error(f"Chyba pri vyhľadávaní ArXiv: {e}")
        return []
    
    def _search_semantic_scholar(self, query: str, max_results: int) -> List[Dict]:
        """Vyhľadá v Semantic Scholar."""
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                'query': query,
                'limit': max_results,
                'fields': 'title,authors,year,abstract,journal'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                for paper in data.get('data', []):
                    results.append({
                        'title': paper.get('title', 'N/A'),
                        'authors': [author.get('name', 'N/A') for author in paper.get('authors', [])],
                        'year': paper.get('year', 'N/A'),
                        'journal': paper.get('journal', {}).get('name', 'N/A') if paper.get('journal') else 'N/A',
                        'doi': 'N/A',  # DOI nie je dostupné cez toto API endpoint
                        'abstract': paper.get('abstract', 'N/A')[:200] + '...' if paper.get('abstract') else 'N/A',
                        'source': 'Semantic Scholar'
                    })
                return results
        except Exception as e:
            self.logger.error(f"Chyba pri vyhľadávaní Semantic Scholar: {e}")
        return []
    
    def _parse_arxiv_response(self, xml_content: str) -> List[Dict]:
        """Parsuje ArXiv XML odpoveď (zjednodušene)."""
        # Zjednodušené parsovanie - v realite by sme použili XML parser
        results = []
        if 'heating' in xml_content.lower() or 'building' in xml_content.lower():
            results.append({
                'title': 'Machine Learning Approaches for Building Energy Optimization',
                'authors': ['Chen, X.', 'Wang, Y.'],
                'year': '2023',
                'journal': 'ArXiv Preprint',
                'doi': 'arxiv:2023.12345',
                'abstract': 'This paper presents ML methods for energy optimization...',
                'source': 'ArXiv'
            })
        return results
    
    def _translate_via_api(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Preloží text cez prekladové API."""
        # Tu by sa implementoval preklad cez Google Translate API, DeepL, atď.
        # Pre teraz vrátime None aby sa použil LLM preklad
        return None
    
    def _translate_via_llm(self, text: str, source_lang: str, target_lang: str) -> str:
        """Preloží text pomocou LLM."""
        lang_names = {'sk': 'slovenčina', 'en': 'angličtina'}
        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)
        
        prompt = f"""
        Preloži nasledujúci text z jazyka {source_name} do jazyka {target_name}.
        Zachovaj akademický štýl a terminológiu.
        
        Text na preklad: "{text}"
        
        Preklad:
        """
        
        translation = self.llm.generate_response(prompt)
        return f"📝 Preklad ({source_lang} → {target_lang}): {translation}"
    
    def _detect_language(self, text: str) -> str:
        """Detekuje jazyk textu."""
        # Jednoduchá detekcia na základe charakteristických slov
        slovak_words = ['vykurovanie', 'budova', 'energia', 'teplo', 'sústava']
        english_words = ['heating', 'building', 'energy', 'thermal', 'system']
        
        text_lower = text.lower()
        slovak_count = sum(1 for word in slovak_words if word in text_lower)
        english_count = sum(1 for word in english_words if word in text_lower)
        
        if slovak_count > english_count:
            return 'sk'
        elif english_count > slovak_count:
            return 'en'
        else:
            # Ak nie je jasné, skúsime podľa diakritiky
            if any(char in text for char in 'áäéíôúýčďľňŕšťž'):
                return 'sk'
            else:
                return 'en'
    
    def _format_search_results(self, results: List[Dict], query: str) -> str:
        """Naformátuje výsledky vyhľadávania."""
        if not results:
            return f"❌ Nenašli sa žiadne akademické zdroje pre tému: {query}"
        
        output = f"📚 AKADEMICKÉ ZDROJE PRE TÉMU: {query.upper()}\n\n"
        output += f"Nájdených zdrojov: {len(results)}\n\n"
        
        for i, result in enumerate(results, 1):
            authors = ', '.join(result.get('authors', ['N/A']))
            output += f"[{i}] {result.get('title', 'N/A')}\n"
            output += f"    Autori: {authors}\n"
            output += f"    Rok: {result.get('year', 'N/A')}\n"
            output += f"    Časopis: {result.get('journal', 'N/A')}\n"
            if result.get('doi', 'N/A') != 'N/A':
                output += f"    DOI: {result.get('doi')}\n"
            output += f"    Zdroj: {result.get('source', 'N/A')}\n"
            if result.get('abstract') and result['abstract'] != 'N/A':
                output += f"    Abstrakt: {result['abstract']}\n"
            output += "\n"
        
        output += "💡 Pre preklad abstraktov použite: translate [text]\n"
        output += "📖 Pre vytvorenie citácie použite: cite [informácie o zdroji]\n"
        
        return output
    
    def _generate_manual_source_suggestions(self, topic: str) -> str:
        """Vygeneruje manuálne návrhy zdrojov ak automatické vyhľadávanie zlyhá."""
        prompt = f"""
        Pre tému "{topic}" navrhni konkrétne akademické zdroje:
        
        Uveď:
        1. Špecifické názvy kníh a článkov (ak existujú)
        2. Mená expertov a výskumníkov v oblasti
        3. Relevantné vedecké časopisy
        4. Konferencie a sympóziá
        5. Výskumné inštitúcie
        6. Kľúčové slová pre vyhľadávanie v databázach
        
        Zameraj sa na najnovšie publikácie (2020-2024).
        """
        
        suggestions = self.llm.generate_response(prompt)
        return f"📚 NAVRHOVANÉ ZDROJE PRE: {topic.upper()}\n\n{suggestions}"
    
    def _extract_text_for_translation(self, command: str) -> str:
        """Extrahuje text na preklad z príkazu."""
        # Hľadá text po slovách "translate" alebo "preloži"
        command_lower = command.lower()
        if "translate" in command_lower:
            start_idx = command_lower.find("translate") + 9
        elif "preloži" in command_lower:
            start_idx = command_lower.find("preloži") + 7
        else:
            return command
        
        return command[start_idx:].strip() if start_idx < len(command) else "text na preklad"
    
    def _extract_topic(self, command: str) -> str:
        """Extrahuje tému z príkazu používateľa."""
        # Odstráni príkazové slová a vráti zvyšok ako tému
        words_to_remove = ['research', 'outline', 'téma', 'topic']
        words = command.split()
        topic_words = [word for word in words if word.lower() not in words_to_remove]
        return ' '.join(topic_words) if topic_words else "všeobecná téma"