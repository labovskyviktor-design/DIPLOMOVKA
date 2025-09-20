"""
Thesis AI Agent - Core Agent Implementation

This module contains the main ThesisAIAgent class that provides various
functionalities to assist with thesis writing and research.
"""

import logging
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

from .llm_interface import LLMInterface
from .document_processor import DocumentProcessor
from .research_assistant import ResearchAssistant
from .writing_assistant import WritingAssistant
from .citation_manager import CitationManager


class ThesisAIAgent:
    """
    Main AI agent class for thesis assistance.
    
    This agent provides comprehensive support for thesis writing including:
    - Research assistance and literature review
    - Writing and editing support
    - Citation management
    - Document processing and analysis
    - Outline generation and structuring
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Thesis AI Agent.
        
        Args:
            config: Configuration dictionary containing settings and API keys
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.llm = LLMInterface(config.get('llm', {}))
        self.doc_processor = DocumentProcessor()
        self.research_assistant = ResearchAssistant(self.llm, config.get('research', {}))
        self.writing_assistant = WritingAssistant(self.llm)
        self.citation_manager = CitationManager()
        
        self.logger.info("Thesis AI Agent initialized with all components")
    
    def run_interactive(self):
        """Run the agent in interactive mode with a command-line interface."""
        self.logger.info("Starting interactive mode")
        print("🎓 Thesis AI Agent - Interactive Mode")
        print("Type 'help' for available commands, 'quit' to exit\\n")
        
        while True:
            try:
                user_input = input("📝 > ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Good luck with your thesis!")
                    break
                    
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # Process the user's request
                response = self._process_command(user_input)
                print(f"\\n🤖 {response}\\n")
                
            except KeyboardInterrupt:
                print("\\n👋 Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Error in interactive mode: {e}")
                print(f"❌ An error occurred: {e}")
    
    def run_batch(self, input_file: str):
        """
        Run the agent in batch mode processing a file of commands.
        
        Args:
            input_file: Path to file containing commands to process
        """
        self.logger.info(f"Starting batch mode with file: {input_file}")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                commands = f.readlines()
            
            results = []
            for i, command in enumerate(commands, 1):
                command = command.strip()
                if command and not command.startswith('#'):
                    self.logger.info(f"Processing command {i}: {command}")
                    result = self._process_command(command)
                    results.append(f"Command {i}: {command}\\nResult: {result}\\n")
            
            # Save results
            output_file = f"batch_results_{Path(input_file).stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\\n".join(results))
            
            print(f"✅ Batch processing completed. Results saved to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Error in batch mode: {e}")
            print(f"❌ Batch processing failed: {e}")
    
    def run_web_interface(self):
        """Run the agent with a web-based interface using Streamlit."""
        try:
            import streamlit as st
            from .web_interface import create_streamlit_app
            
            self.logger.info("Starting web interface")
            create_streamlit_app(self)
            
        except ImportError:
            print("❌ Streamlit not installed. Install with: pip install streamlit")
        except Exception as e:
            self.logger.error(f"Error starting web interface: {e}")
            print(f"❌ Failed to start web interface: {e}")
    
    def _process_command(self, command: str) -> str:
        """
        Process a user command and return the response.
        
        Args:
            command: User input command
            
        Returns:
            Response from the appropriate agent component
        """
        command_lower = command.lower()
        
        # Research-related commands
        if command_lower.startswith('research'):
            return self.research_assistant.handle_research_query(command)
        
        # Writing-related commands
        elif any(word in command_lower for word in ['write', 'edit', 'improve', 'draft']):
            return self.writing_assistant.handle_writing_query(command)
        
        # Citation-related commands
        elif any(word in command_lower for word in ['cite', 'reference', 'bibliography']):
            return self.citation_manager.handle_citation_query(command)
        
        # Document processing commands
        elif any(word in command_lower for word in ['analyze', 'summarize', 'process']):
            return self.doc_processor.handle_document_query(command)
        
        # General queries - use the main LLM
        else:
            return self.llm.generate_response(
                f"As a thesis writing assistant, please help with: {command}"
            )
    
    def _show_help(self):
        """Display help information for available commands."""
        help_text = """
📖 Available Commands:

Research Commands:
  • research [topic] - Find relevant papers and sources
  • search [topic] / hľadaj [téma] - Search academic databases
  • translate [text] / preloži [text] - Translate academic texts
  • research outline [topic] - Generate research outline
  
Writing Commands:
  • write introduction [topic] - Draft introduction section
  • write conclusion [topic] - Draft conclusion section
  • edit [text] - Improve and edit text
  • improve [section] - Enhance writing quality
  
Citation Commands:
  • cite [source] - Generate citation
  • bibliography - Manage references
  • reference [topic] - Find citation format
  
Document Commands:
  • analyze [file] - Analyze document content
  • summarize [file] - Create document summary
  • process [file] - Extract key information

General:
  • help - Show this help message
  • quit - Exit the application
        """
        print(help_text)
