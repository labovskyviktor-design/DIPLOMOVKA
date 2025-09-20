"""
Configuration management for the Thesis AI Agent.
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file with environment variable overrides.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    
    # Default configuration
    default_config = {
        "llm": {
            "provider": "openai",  # or "anthropic"
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000
        },
        "research": {
            "max_sources": 10,
            "search_depth": "moderate"
        },
        "writing": {
            "style": "academic",
            "citation_format": "APA"
        },
        "output": {
            "format": "markdown",
            "save_history": True
        }
    }
    
    # Load from file if it exists
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f) or {}
            # Merge with default config
            default_config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    else:
        print(f"Config file {config_path} not found, using defaults")
    
    # Override with environment variables
    _apply_env_overrides(default_config)
    
    return default_config


def _apply_env_overrides(config: Dict[str, Any]) -> None:
    """Apply environment variable overrides to configuration."""
    
    # API Keys
    if os.getenv("OPENAI_API_KEY"):
        config.setdefault("llm", {})["openai_api_key"] = os.getenv("OPENAI_API_KEY")
    
    if os.getenv("ANTHROPIC_API_KEY"):
        config.setdefault("llm", {})["anthropic_api_key"] = os.getenv("ANTHROPIC_API_KEY")
    
    # Model overrides
    if os.getenv("LLM_MODEL"):
        config.setdefault("llm", {})["model"] = os.getenv("LLM_MODEL")
    
    if os.getenv("LLM_PROVIDER"):
        config.setdefault("llm", {})["provider"] = os.getenv("LLM_PROVIDER")


def save_config(config: Dict[str, Any], config_path: str = "config/config.yaml") -> None:
    """
    Save configuration to YAML file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the configuration
    """
    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        print(f"Configuration saved to {config_path}")
    except Exception as e:
        print(f"Error saving config to {config_path}: {e}")