"""
Správca citácií a bibliografie pre dizertačnú prácu.
"""

import logging
from typing import Dict, List, Any


class CitationManager:
    """Správca citácií v rôznych formátoch (APA, MLA, Chicago)."""
    
    def __init__(self):
        """Inicializácia správcu citácií."""
        self.logger = logging.getLogger(__name__)
        self.citations = []  # Uložené citácie
        
    def handle_citation_query(self, command: str) -> str:
        """
        Spracuje dotaz týkajúci sa citácií.
        
        Args:
            command: Príkaz od používateľa
            
        Returns:
            Odpoveď správcu citácií
        """
        command_lower = command.lower()
        
        if "bibliography" in command_lower or "bibliografia" in command_lower:
            return self.generate_bibliography()
        elif "cite" in command_lower or "cituj" in command_lower:
            source = self._extract_source(command)
            return self.create_citation(source)
        elif "format" in command_lower or "formát" in command_lower:
            return self.show_citation_formats()
        else:
            return "Dostupné príkazy: cite [zdroj], bibliography, format [štýl]"
    
    def create_citation(self, source_info: str, style: str = "STN") -> str:
        """
        Vytvorí citáciu v požadovanom formáte.
        
        Args:
            source_info: Informácie o zdroji
            style: Štýl citácie (STN, APA, MLA, Chicago)
            
        Returns:
            Formátovaná citácia
        """
        if style.upper() in ["STN", "ISO", "STN_ISO"]:
            return self._format_stn_iso_citation(source_info)
        elif style.upper() == "APA":
            return self._format_apa_citation(source_info)
        elif style.upper() == "MLA":
            return self._format_mla_citation(source_info)
        elif style.upper() == "CHICAGO":
            return self._format_chicago_citation(source_info)
        else:
            return f"Nepodporovaný štýl citácie: {style}. Podporované: STN/ISO, APA, MLA, Chicago"
    
    def _format_stn_iso_citation(self, source_info: str) -> str:
        """Formátuje citáciu v STN ISO 690 štýle."""
        return f"""
STN ISO 690 Citácia:
Pre korektné vytvorenie STN ISO 690 citácie potrebujem:

Knihy/monografie:
- PRIEZVISKO, M. Názov publikácie. Miesto vydania : Vydavateľ, rok. ISBN.
- Príklad: OBERT, V. Návraty a odkazy. Nitra : Univerzita Konštantína Filozofa, 2006. 129 s. ISBN 80-8094-046-0.

Článok v časopise:
- PRIEZVISKO, M. Názov článku. Názov časopisu. Rok, roč. x, č. y, s. z-w. ISSN.
- Príklad: STEINEROVÁ, J. Princípy formovania vzdelania v informačnej vede. In Pedagogická revue. ISSN 1335-1982, 2000, roč. 2, č. 3, s. 8-16.

Elektronické dokumenty:
- PRIEZVISKO, M. Názov. [online]. Miesto : Vydavateľ, rok. [cit. YYYY-MM-DD]. Dostupné na internete: <URL>. ISBN.

V texte sa cituje číslom v hranatých zátvorkách [1], [2], atď.

Poskytnuté informácie: {source_info}

Prosím doplňte chýbajúce údaje pre presnejšiu citáciu.
        """
    
    def _format_apa_citation(self, source_info: str) -> str:
        """Formátuje citáciu v APA štýle."""
        return f"""
APA Citácia:
Pre korektné vytvorenie APA citácie potrebujem:
- Meno autora (Priezvisko, M. M.)
- Rok publikácie (YYYY)
- Názov diela
- Vydavateľ/Časopis
- DOI alebo URL (ak je dostupné)

Príklad: Smith, J. A. (2023). Názov článku. Journal Name, 15(3), 45-67. https://doi.org/10.xxxx

Poskytnuté informácie: {source_info}

Prosím doplňte chýbajúce údaje pre presnejšiu citáciu.
        """
    
    def _format_mla_citation(self, source_info: str) -> str:
        """Formátuje citáciu v MLA štýle."""
        return f"""
MLA Citácia:
Pre korektné vytvorenie MLA citácie potrebujem:
- Meno autora (Priezvisko, Meno)
- Názov diela (v uvodzovkách alebo kurzívou)
- Názov kontajnera (časopis, kniha)
- Vydavateľ
- Dátum publikácie
- Umiestnenie (strany, URL)

Príklad: Smith, John A. "Názov článku." Journal Name, vol. 15, no. 3, 2023, pp. 45-67.

Poskytnuté informácie: {source_info}

Prosím doplňte chýbajúce údaje pre presnejšiu citáciu.
        """
    
    def _format_chicago_citation(self, source_info: str) -> str:
        """Formátuje citáciu v Chicago štýle."""
        return f"""
Chicago Citácia:
Pre korektné vytvorenie Chicago citácie potrebujem:
- Meno autora (Priezvisko, Meno)
- Názov diela
- Miesto publikácie
- Vydavateľ
- Rok publikácie

Príklad: Smith, John A. "Názov článku." Journal Name 15, no. 3 (2023): 45-67.

Poskytnuté informácie: {source_info}

Prosím doplňte chýbajúce údaje pre presnejšiu citáciu.
        """
    
    def generate_bibliography(self) -> str:
        """
        Vytvorí zoznam literatúry zo všetkých uložených citácií.
        
        Returns:
            Formátovaná bibliografia
        """
        if not self.citations:
            return """
📚 Bibliografia je momentálne prázdna.

Pre pridanie citácií použite príkaz: cite [informácie o zdroji]

Príklady:
- cite Smith, J. (2023). Názov knihy. Vydavateľstvo
- cite "Názov článku" Journal Name 2023
            """
        
        bibliography = "📚 BIBLIOGRAFIA\n\n"
        for i, citation in enumerate(self.citations, 1):
            bibliography += f"{i}. {citation}\n\n"
        
        return bibliography
    
    def add_citation(self, citation: str) -> str:
        """
        Pridá citáciu do zoznamu.
        
        Args:
            citation: Formátovaná citácia
            
        Returns:
            Potvrdenie o pridaní
        """
        self.citations.append(citation)
        return f"✅ Citácia pridaná do bibliografie. Celkový počet: {len(self.citations)}"
    
    def show_citation_formats(self) -> str:
        """Zobrazí dostupné formáty citácií s príkladmi."""
        return """
📖 FORMÁTY CITÁCIÍ

🔹 STN ISO 690 (Slovenská technická norma - predvolený)
   Kniha: OBERT, V. Návraty a odkazy. Nitra : Univerzita Konštantína Filozofa, 2006. 129 s. ISBN 80-8094-046-0.
   Článok: STEINEROVÁ, J. Princípy formovania vzdelania v informačnej vede. In Pedagogická revue. ISSN 1335-1982, 2000, roč. 2, č. 3, s. 8-16.
   Citovanie v texte: [1], [2], atď.

🔹 APA (American Psychological Association)
   Kniha: Smith, J. A. (2023). Názov knihy. Vydavateľstvo.
   Článok: Smith, J. A. (2023). Názov článku. Journal Name, 15(3), 45-67.

🔹 MLA (Modern Language Association)
   Kniha: Smith, John A. Názov knihy. Vydavateľstvo, 2023.
   Článok: Smith, John A. "Názov článku." Journal Name, vol. 15, no. 3, 2023, pp. 45-67.

🔹 Chicago (Chicago Manual of Style)
   Kniha: Smith, John A. Názov knihy. Miesto: Vydavateľstvo, 2023.
   Článok: Smith, John A. "Názov článku." Journal Name 15, no. 3 (2023): 45-67.

Pre vytvorenie citácie použite: cite [informácie] format [štýl]
        """
    
    def validate_citation(self, citation: str, style: str = "APA") -> str:
        """
        Overí správnosť formátu citácie.
        
        Args:
            citation: Citácia na overenie
            style: Štýl citácie
            
        Returns:
            Hodnotenie a návrhy na zlepšenie
        """
        return f"""
🔍 OVERENIE CITÁCIE ({style} štýl)

Citácia: {citation}

⚠️ Pre úplné overenie by som potreboval špecializovaný nástroj.

Základné kontroly:
✓ Skontrolujte interpunkciu
✓ Overí poradie informácií
✓ Skontrolujte kurzívu/úvodzovky
✓ Overí dátumy a čísla strán

Odporúčam použiť špecializovaný nástroj ako Zotero, Mendeley alebo oficiálne štýlové príručky.
        """
    
    def _extract_source(self, command: str) -> str:
        """Extrahuje informácie o zdroji z príkazu."""
        # Odstráni príkazové slová
        words_to_remove = ['cite', 'cituj', 'format', 'formát']
        words = command.split()
        source_words = [word for word in words if word.lower() not in words_to_remove]
        return ' '.join(source_words) if source_words else "neurčený zdroj"