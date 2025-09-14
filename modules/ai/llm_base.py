"""
Base LLM Interface
Defines the protocol for LLM implementations
"""

from typing import Optional, Dict, List, Protocol

class LLM(Protocol):
    """
    Protocol for LLM implementations
    """
    def generate(self, prompt: str, system: Optional[str] = None, options: Optional[Dict] = None, images: Optional[List[str]] = None) -> str:
        """
        Generate text response from LLM

        Args:
            prompt: The main prompt text
            system: Optional system message/instruction
            options: Optional generation parameters (temperature, max_tokens, etc.)
            images: Optional list of image file paths for vision models

        Returns:
            Generated text response
        """
        ...
