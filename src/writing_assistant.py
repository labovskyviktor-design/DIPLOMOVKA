"""
Asistent pre písanie a úpravu textu dizertačnej práce.
"""

import logging
from typing import Dict, List, Any


class WritingAssistant:
    """Asistent pre písanie a editáciu akademických textov."""
    
    def __init__(self, llm_interface):
        """
        Inicializácia asistenta písania.
        
        Args:
            llm_interface: Rozhranie pre jazykový model
        """
        self.llm = llm_interface
        self.logger = logging.getLogger(__name__)
        
    def handle_writing_query(self, command: str) -> str:
        """
        Spracuje dotaz týkajúci sa písania.
        
        Args:
            command: Príkaz od používateľa
            
        Returns:
            Odpoveď asistenta písania
        """
        command_lower = command.lower()
        
        if "introduction" in command_lower or "úvod" in command_lower:
            topic = self._extract_topic(command)
            return self.write_introduction(topic)
        elif "conclusion" in command_lower or "záver" in command_lower:
            topic = self._extract_topic(command)
            return self.write_conclusion(topic)
        elif "edit" in command_lower or "improve" in command_lower:
            text = self._extract_text(command)
            return self.improve_text(text)
        elif "draft" in command_lower or "náčrt" in command_lower:
            topic = self._extract_topic(command)
            return self.create_draft(topic)
        else:
            return self.llm.generate_response(f"Asistent písania: {command}")
    
    def write_introduction(self, topic: str) -> str:
        """
        Napíše úvodná sekciu pre danú tému.
        
        Args:
            topic: Téma úvodu
            
        Returns:
            Napísaný úvod
        """
        prompt = f"""
        Napíš akademický úvod pre tému: "{topic}"
        
        Úvod by mal obsahovať:
        1. Kontext a pozadie témy
        2. Dôležitosť a relevantnosť výskumu
        3. Hlavné výskumné otázky
        4. Ciele a prínosy práce
        5. Štruktúru práce
        
        Používaj formálny akademický štýl. Dĺžka: 300-500 slov.
        """
        
        return self.llm.generate_response(prompt)
    
    def write_conclusion(self, topic: str) -> str:
        """
        Napíše záverečnú sekciu.
        
        Args:
            topic: Téma záveru
            
        Returns:
            Napísaný záver
        """
        prompt = f"""
        Napíš akademický záver pre tému: "{topic}"
        
        Záver by mal obsahovať:
        1. Zhrnutie hlavných zistení
        2. Príspevok k existujúcemu poznaniu
        3. Praktické implikácie
        4. Obmedzenia výskumu
        5. Návrhy na ďalší výskum
        
        Používaj formálny akademický štýl. Dĺžka: 200-400 slov.
        """
        
        return self.llm.generate_response(prompt)
    
    def improve_text(self, text: str) -> str:
        """
        Zlepší a upraví existujúci text.
        
        Args:
            text: Text na úpravu
            
        Returns:
            Zlepšený text
        """
        prompt = f"""
        Zlepši nasledujúci akademický text:

        "{text}"

        Zameraj sa na:
        1. Gramatiku a syntax
        2. Jasnosť a zrozumiteľnosť
        3. Akademický štýl
        4. Logickú štruktúru
        5. Súdržnosť argumentov

        Vráť zlepšenú verziu s krátkym komentárom o vykonaných zmenách.
        """
        
        return self.llm.generate_response(prompt)
    
    def create_draft(self, topic: str) -> str:
        """
        Vytvorí prvotný náčrt pre danú tému.
        
        Args:
            topic: Téma náčrtu
            
        Returns:
            Vytvorený náčrt
        """
        prompt = f"""
        Vytvor prvotný náčrt akademického textu pre tému: "{topic}"
        
        Náčrt by mal obsahovať:
        1. Základnú štruktúru (nadpisy a podnadpisy)
        2. Stručný obsah každej sekcie
        3. Hlavné argumenty a body
        4. Prepojenia medzi sekciami
        5. Približný rozsah každej časti
        
        Formátuj ako obrys s poznámkami.
        """
        
        return self.llm.generate_response(prompt)
    
    def check_style(self, text: str, style: str = "academic") -> str:
        """
        Skontroluje štýl písania.
        
        Args:
            text: Text na kontrolu
            style: Požadovaný štýl (academic, formal, casual)
            
        Returns:
            Hodnotenie štýlu a návrhy
        """
        prompt = f"""
        Skontroluj štýl nasledujúceho textu a posuď, či zodpovedá {style} štýlu:

        "{text}"

        Poskytni:
        1. Celkové hodnotenie štýlu (1-10)
        2. Silné stránky
        3. Oblasti na zlepšenie
        4. Konkrétne návrhy zmien
        5. Príklady lepšieho formuovania
        """
        
        return self.llm.generate_response(prompt)
    
    def _extract_topic(self, command: str) -> str:
        """Extrahuje tému z príkazu používateľa."""
        # Odstráni príkazové slová
        words_to_remove = ['write', 'introduction', 'conclusion', 'draft', 'úvod', 'záver', 'náčrt']
        words = command.split()
        topic_words = [word for word in words if word.lower() not in words_to_remove]
        return ' '.join(topic_words) if topic_words else "všeobecná téma"
    
    def _extract_text(self, command: str) -> str:
        """Extrahuje text z príkazu používateľa."""
        # Hľadá text po slovách "edit" alebo "improve"
        command_lower = command.lower()
        if "edit" in command_lower:
            start_idx = command_lower.find("edit") + 4
        elif "improve" in command_lower:
            start_idx = command_lower.find("improve") + 7
        else:
            return command
        
        return command[start_idx:].strip() if start_idx < len(command) else "text na úpravu"