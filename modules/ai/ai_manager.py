"""
AI Manager
Factory for creating configured LLM instances
"""

from typing import Optional
from .ollama_client import OllamaLLM

# Cache for LLM instance
_cached_llm = None

def get_llm():
    """
    Get configured LLM instance

    Returns:
        LLM instance based on configuration
    """
    global _cached_llm
    if _cached_llm:
        return _cached_llm

    # Import config here to avoid circular imports
    from config import AI_PROVIDER, OLLAMA_CONFIG

    provider = (AI_PROVIDER or "ollama").lower()

    if provider == "ollama":
        cfg = OLLAMA_CONFIG
        _cached_llm = OllamaLLM(
            model=cfg.get("model", "gemma3:4b"),
            host=cfg.get("host"),
            default_options=cfg.get("options", {}),
            timeout_s=cfg.get("timeout_s", 30),
            max_retries=cfg.get("max_retries", 2),
        )
        return _cached_llm

    raise ValueError(f"Unsupported AI provider: {provider}")
