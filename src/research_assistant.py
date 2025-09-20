"""
Výskumný asistent pre vyhľadávanie a analýzu zdrojov.
"""

import logging
from typing import Dict, List, Any


class ResearchAssistant:
    """Asistent pre výskumnú činnosť a literatúru."""
    
    def __init__(self, llm_interface):
        """
        Inicializácia výskumného asistenta.
        
        Args:
            llm_interface: Rozhranie pre jazykový model
        """
        self.llm = llm_interface
        self.logger = logging.getLogger(__name__)
        
    def handle_research_query(self, command: str) -> str:
        """
        Spracuje výskumný dotaz.
        
        Args:
            command: Príkaz od používateľa
            
        Returns:
            Výskumná odpoveď
        """
        command_lower = command.lower()
        
        if "outline" in command_lower:
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
    
    def _extract_topic(self, command: str) -> str:
        """Extrahuje tému z príkazu používateľa."""
        # Odstráni príkazové slová a vráti zvyšok ako tému
        words_to_remove = ['research', 'outline', 'téma', 'topic']
        words = command.split()
        topic_words = [word for word in words if word.lower() not in words_to_remove]
        return ' '.join(topic_words) if topic_words else "všeobecná téma"