"""
LLM Interface module for connecting to various language models.
"""

from typing import Dict, Any
import logging


class LLMInterface:
    """Interface for Large Language Models (OpenAI, Anthropic, etc.)"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the LLM interface with configuration."""
        self.config = config
        self.provider = config.get('provider', 'openai')
        self.model = config.get('model', 'gpt-4')
        self.logger = logging.getLogger(__name__)
        
        # Initialize the appropriate client based on provider
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LLM client based on the configured provider."""
        try:
            if self.provider == 'openai':
                import openai
                self.client = openai.OpenAI(
                    api_key=self.config.get('openai_api_key')
                )
            elif self.provider == 'anthropic':
                import anthropic
                self.client = anthropic.Anthropic(
                    api_key=self.config.get('anthropic_api_key')
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
                
            self.logger.info(f"Initialized {self.provider} client with model {self.model}")
            
        except ImportError as e:
            self.logger.error(f"Required library not installed for {self.provider}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.provider} client: {e}")
            raise
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The input prompt for the model
            **kwargs: Additional parameters for the model
            
        Returns:
            Generated response text
        """
        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.get('temperature', 0.7),
                    max_tokens=self.config.get('max_tokens', 2000),
                    **kwargs
                )
                return response.choices[0].message.content
                
            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.config.get('max_tokens', 2000),
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.get('temperature', 0.7),
                    **kwargs
                )
                return response.content[0].text
                
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"