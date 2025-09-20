# 🎓 Thesis AI Agent

Vlastný AI agent pre pomoc s písaním dizertačnej práce - komplexný nástroj na podporu akademického písania, výskumu a citovania.

## 📋 Obsah

- [Funkcie](#funkcie)
- [Inštalácia](#inštalácia)
- [Konfigurácia](#konfigurácia)
- [Použitie](#použitie)
- [Príklady](#príklady)
- [Štruktúra projektu](#štruktúra-projektu)
- [Prispievanie](#prispievanie)

## ✨ Funkcie

### 🔍 Výskumný asistent
- Generovanie výskumných návrhov a outline
- Vyhľadávanie relevantných zdrojov a literatúry
- Analýza medzier v poznávaní
- Návrhy výskumných otázok

### ✍️ Asistent písania
- Písanie úvodov, záverov a náčrtov
- Zlepšovanie a editácia existujúceho textu
- Kontrola akademického štýlu
- Štruktúrovanie obsahu

### 📚 Správa citácií
- Podpora viacerých formátov (APA, MLA, Chicago)
- Generovanie bibliografie
- Validácia citácií
- Správa zdrojov

### 📄 Spracovanie dokumentov
- Podpora PDF, DOCX, TXT, MD súborov
- Extrakcia a analýza obsahu
- Zhrňovanie dokumentov
- Spracovanie metadát

## 🚀 Inštalácia

### Požiadavky
- Python 3.8+
- OpenAI API kľúč alebo Anthropic API kľúč

### Kroky inštalácie

1. **Klonujte repozitár:**
   ```bash
   git clone <repository-url>
   cd thesis-ai-agent
   ```

2. **Vytvorte virtuálne prostredie:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Nainštalujte závislosti:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Nastavte API kľúče:**
   ```bash
   # Pre OpenAI
   set OPENAI_API_KEY=your_api_key_here
   
   # Pre Anthropic
   set ANTHROPIC_API_KEY=your_api_key_here
   ```

## ⚙️ Konfigurácia

Nastavenia sa nachádzajú v `config/config.yaml`. Môžete upraviť:

- **LLM nastavenia**: poskytovateľ, model, teplota
- **Výskumné parametre**: počet zdrojov, hĺbka vyhľadávania  
- **Štýl písania**: akademický štýl, formát citácií
- **Výstupné formáty**: markdown, docx, pdf

### Príklad konfigurácie:
```yaml
llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.7

writing:
  style: "academic"
  citation_format: "APA"
  language: "sk"
```

## 📖 Použitie

### Interaktívny režim
```bash
python main.py --mode interactive
```

### Webové rozhranie  
```bash
python main.py --mode web
```

### Dávkové spracovanie
```bash
python main.py --mode batch --input-file commands.txt
```

## 💡 Príklady

### Výskumné príkazy
```
research umelá inteligencia v zdravotníctve
research outline strojové učenie
```

### Písanie
```  
write introduction kvantové počítačstvo
edit "Môj text na zlepšenie..."
improve abstract section
```

### Citácie
```
cite Smith, J. (2023). AI in Healthcare
bibliography
format APA
```

### Dokumenty
```
analyze document.pdf  
summarize research_paper.docx
process thesis_draft.md
```

## 📁 Štruktúra projektu

```
thesis-ai-agent/
├── main.py                 # Hlavný vstupný bod
├── requirements.txt        # Python závislosti
├── README.md              # Dokumentácia
├── .gitignore             # Git ignorované súbory
├── config/                # Konfiguračné súbory
│   └── config.yaml        # Hlavná konfigurácia
├── src/                   # Zdrojový kód
│   ├── __init__.py
│   ├── agent.py           # Hlavná trieda agenta
│   ├── config.py          # Správa konfigurácie
│   ├── llm_interface.py   # Rozhranie pre LLM
│   ├── research_assistant.py    # Výskumný asistent  
│   ├── writing_assistant.py     # Asistent písania
│   ├── citation_manager.py      # Správa citácií
│   └── document_processor.py    # Spracovanie dokumentov
├── docs/                  # Dokumentácia
├── tests/                 # Testy
└── outputs/              # Výstupné súbory
```

## 🎯 Dostupné príkazy

### Všeobecné
- `help` - Zobrazí nápovedu
- `quit` - Ukončí program

### Výskum  
- `research [téma]` - Výskum témy
- `research outline [téma]` - Vytvorí outline

### Písanie
- `write introduction [téma]` - Napíše úvod
- `write conclusion [téma]` - Napíše záver  
- `edit [text]` - Zlepší text
- `draft [téma]` - Vytvorí náčrt

### Citácie
- `cite [zdroj]` - Vytvorí citáciu
- `bibliography` - Zobrazí bibliografiu
- `format [štýl]` - Zobrazí formáty

### Dokumenty
- `analyze [súbor]` - Analyzuje dokument
- `summarize [súbor]` - Zhrnie dokument  
- `process [súbor]` - Spracuje súbor

## 🔧 Vývoj

### Spustenie testov
```bash
pytest tests/
```

### Formátovanie kódu
```bash
black src/
flake8 src/
```

### Pridanie nových funkcií
1. Vytvorte novú vetvú
2. Implementujte funkciu v príslušnom module
3. Pridajte testy
4. Vytvorte pull request

## 🤝 Prispievanie

Príspevky sú vítané! Prosím:

1. Forkujte projekt
2. Vytvorte feature branch (`git checkout -b feature/nova-funkcia`)
3. Commitnite zmeny (`git commit -am 'Pridaj novú funkciu'`)
4. Pushnite do branchu (`git push origin feature/nova-funkcia`)
5. Vytvorte Pull Request

## 📝 Licencia

Tento projekt je licencovaný pod MIT licenciou - pozrite súbor [LICENSE](LICENSE) pre detaily.

## 🆘 Podpora

Ak máte problémy alebo otázky:
- Vytvorte issue na GitHube
- Skontrolujte dokumentáciu v `docs/`
- Pozrite si príklady v `examples/`

## 🚀 Roadmapa

- [ ] Integrácia s Google Scholar API
- [ ] Pokročilé analytické nástroje  
- [ ] Podpora viacerých jazykov
- [ ] Plugin pre Word/LaTeX
- [ ] Grafické používateľské rozhraný
- [ ] Kolaboratívne funkcie

---

**Vytvorené s ❤️ pre akademickú komunitu**