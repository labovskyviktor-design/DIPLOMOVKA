#!/usr/bin/env python3
"""
Thesis AI Agent - Main Entry Point

A custom AI agent designed to assist with thesis writing, research, and analysis.
"""

import argparse
import logging
from pathlib import Path

from src.agent import ThesisAIAgent
from src.config import load_config


def setup_logging(level: str = "INFO"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('thesis_agent.log'),
            logging.StreamHandler()
        ]
    )


def main():
    """Main entry point for the Thesis AI Agent."""
    parser = argparse.ArgumentParser(description="Thesis AI Agent")
    parser.add_argument(
        "--config", 
        type=str, 
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--mode", 
        choices=["interactive", "batch", "web"],
        default="interactive",
        help="Running mode for the agent"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    parser.add_argument(
        "--input-file",
        type=str,
        help="Input file for batch processing"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = load_config(args.config)
        logger.info(f"Loaded configuration from {args.config}")
        
        # Initialize the AI agent
        agent = ThesisAIAgent(config)
        logger.info("Thesis AI Agent initialized successfully")
        
        # Run the agent based on mode
        if args.mode == "interactive":
            agent.run_interactive()
        elif args.mode == "batch" and args.input_file:
            agent.run_batch(args.input_file)
        elif args.mode == "web":
            agent.run_web_interface()
        else:
            logger.error("Invalid mode or missing input file for batch mode")
            return 1
            
    except Exception as e:
        logger.error(f"Error running Thesis AI Agent: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())