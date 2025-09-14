"""
Base LLM Interface
Defines the protocol for LLM implementations
"""

from typing import Optional, Dict, Protocol

class LLM(Protocol):
    """
    Protocol for LLM implementations
    """
    def generate(self, prompt: str, system: Optional[str] = None, options: Optional[Dict] = None) -> str:
        """
        Generate text response from LLM

        Args:
            prompt: The main prompt text
            system: Optional system message/instruction
            options: Optional generation parameters (temperature, max_tokens, etc.)

        Returns:
            Generated text response
        """
        ...
