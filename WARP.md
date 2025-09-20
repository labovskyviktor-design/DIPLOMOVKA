# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Required Environment Variables
```bash
# Set API keys (required)
set OPENAI_API_KEY=your_api_key_here
set ANTHROPIC_API_KEY=your_api_key_here

# Optional overrides
set LLM_MODEL=gpt-4
set LLM_PROVIDER=openai

# Optional API keys for enhanced academic search
set GOOGLE_API_KEY=your_google_api_key  # For Google Scholar
set SERPAPI_KEY=your_serpapi_key        # SerpAPI for better search results
set DEEPL_API_KEY=your_deepl_key        # DeepL for professional translation
```

### Running the Application
```bash
# Interactive mode (default)
python main.py

# Web interface mode
python main.py --mode web

# Batch processing mode
python main.py --mode batch --input-file commands.txt

# With custom config
python main.py --config custom_config.yaml --log-level DEBUG
```

### Testing and Code Quality
```bash
# Run all tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/

# Run single test file
pytest tests/test_specific.py -v
```

## Architecture Overview

### Core Components Architecture

The Thesis AI Agent follows a modular architecture with clear separation of concerns:

**Main Application Flow:**
- `main.py` → `ThesisAIAgent` → Component Handlers → `LLMInterface`

**Key Components:**
1. **ThesisAIAgent (`src/agent.py`)**: Central orchestrator that routes commands to appropriate specialized components
2. **LLMInterface (`src/llm_interface.py`)**: Abstraction layer supporting both OpenAI and Anthropic APIs with unified interface
3. **Specialized Assistants**: Domain-specific handlers for different thesis writing tasks
4. **Configuration System**: YAML-based configuration with environment variable overrides

### Component Interaction Pattern

```
User Input → ThesisAIAgent._process_command() → Route to Specialist:
├── research* → ResearchAssistant
├── search*/hľadaj* → ResearchAssistant.search_academic_sources()
├── translate*/preloži* → ResearchAssistant.translate_text()
├── write*/edit*/improve*/draft* → WritingAssistant  
├── cite*/reference*/bibliography* → CitationManager
├── analyze*/summarize*/process* → DocumentProcessor
└── general queries → LLMInterface (direct)
```

### Specialized Assistant Components

**ResearchAssistant (`src/research_assistant.py`)**
- Handles research queries, outline generation, source suggestions
- **Academic Search**: Real-time search in Google Scholar, Semantic Scholar, ArXiv
- **Translation Services**: Bidirectional Slovak-English translation for academic texts
- **Specialized for Building Heating**: Optimized search terms and databases for HVAC/heating research
- Methods: `research_topic()`, `search_academic_sources()`, `translate_text()`, `generate_research_outline()`, `suggest_sources()`, `analyze_gap()`

**WritingAssistant (`src/writing_assistant.py`)**
- Manages academic writing tasks (introductions, conclusions, editing)
- Methods: `write_introduction()`, `write_conclusion()`, `improve_text()`, `create_draft()`, `check_style()`

**CitationManager (`src/citation_manager.py`)**
- Handles multiple citation formats (STN ISO 690, APA, MLA, Chicago)
- **Default Format**: STN ISO 690 (Slovak technical standard) with numbered citations [1], [2]
- Methods: `create_citation()`, `generate_bibliography()`, `validate_citation()`, format-specific methods

**DocumentProcessor (`src/document_processor.py`)**
- Processes multiple file formats (PDF, DOCX, TXT, MD)
- Methods: `process_document()`, format-specific processors, metadata extraction

### Configuration Architecture

**Configuration Loading Priority:**
1. Default configuration (hardcoded)
2. YAML file configuration (`config/config.yaml`)
3. Environment variable overrides

**Key Configuration Sections:**
- `llm`: Provider, model, temperature, tokens
- `research`: Search parameters, academic databases, translation settings, heating-specific sources
- `writing`: Style, citation format (default: STN ISO 690), language (default: Slovak)
- `documents`: Supported formats, processing limits
- `output`: Format preferences, history settings
- `web`: Interface settings for Streamlit mode

### LLM Provider Abstraction

The `LLMInterface` provides unified access to different AI providers:
- **OpenAI**: Uses `openai.OpenAI()` client with chat completions API
- **Anthropic**: Uses `anthropic.Anthropic()` client with messages API
- **Provider Selection**: Configured via `llm.provider` setting
- **Unified Response Handling**: Both providers return plain text responses through `generate_response()`

### Command Processing Logic

The agent uses keyword-based routing in `_process_command()`:
- Commands are matched against specific keywords (research, write, cite, analyze, etc.)
- Each specialist component has its own command parsing logic
- Fallback to general LLM interface for unmatched queries
- All responses are string-based for consistency

### Running Modes

**Interactive Mode**: CLI-based REPL with command processing loop
**Batch Mode**: File-based command processing with result saving
**Web Mode**: Streamlit-based GUI (requires `streamlit` package)

## Language and Localization Notes

This codebase contains mixed language content:
- **Primary Interface**: Slovak language for user-facing content and prompts
- **Code/Comments**: Mix of English and Slovak
- **Configuration**: English keys, Slovak documentation
- **Command Keywords**: Support both English and Slovak terms (e.g., "research" and "výskum")
- **Citation Standard**: STN ISO 690 (Slovak technical standard) is the default format
- **Citation Style**: Numbered references [1], [2] in text with full bibliography at end

When working with this codebase, maintain consistency with existing language patterns in each component.

## Development Patterns

### Error Handling
- Use try-catch blocks with detailed logging via `self.logger`
- Return error dictionaries from processing methods: `{"error": "message"}`
- Graceful degradation for missing dependencies (ImportError handling)

### Method Naming Convention
- Private methods use underscore prefix: `_extract_topic()`, `_process_pdf()`
- Handler methods follow pattern: `handle_[component]_query()`
- Format-specific methods: `_format_[style]_citation()`

### Dependency Management
- Optional dependencies handled with ImportError exceptions
- Core dependencies in requirements.txt include AI libraries, document processing, and web frameworks
- Development tools specified separately (pytest, black, flake8)

### File Processing
- Support for multiple formats with unified processing interface
- Metadata extraction included in all document processing results
- File path validation and existence checking in all processors

### Citation Standards
- **Default Format**: STN ISO 690 (010197):2012 Slovak technical standard
- **In-text Citations**: Numbered format [1], [2], [3] etc.
- **Bibliography Format**: Follows Slovak academic conventions with specific punctuation and ordering
- **Supported Types**: Books/monographs, journal articles, electronic documents, conference proceedings
- **Alternative Formats**: APA, MLA, Chicago also supported but STN ISO 690 is primary

### Academic Search Capabilities
- **Real-time Search**: Live queries to academic databases (Google Scholar, Semantic Scholar, ArXiv)
- **Specialized Databases**: Focused on building heating, HVAC, energy efficiency research
- **Multi-language Support**: Search in both Slovak and English with automatic query translation
- **Result Formatting**: Structured output with DOI, abstracts, and citation-ready format
- **Search Providers**: Google Scholar (via scholarly), Semantic Scholar API, ArXiv API
- **Fallback System**: Manual expert suggestions when API search fails

### Translation Services
- **Bidirectional Translation**: Slovak ↔ English for academic texts
- **Academic Terminology**: Preserves technical terms and scientific language
- **Multiple Backends**: LLM-based translation with API fallback options (Google Translate, DeepL)
- **Smart Language Detection**: Automatic source language identification
- **Translation Cache**: Caches translations to improve performance
- **Command Support**: Both English ("translate") and Slovak ("preloži") commands
