"""
Ollama LLM Client
Implements LLM interface using local Ollama
"""

import logging
import time
import os
import ollama
from typing import Optional, Dict
from .llm_base import LLM

class OllamaLLM(LLM):
    """
    LLM implementation using Ollama
    """

    def __init__(self, model: str, host: Optional[str] = None, default_options: Optional[Dict] = None,
                 timeout_s: int = 30, max_retries: int = 2):
        """
        Initialize Ollama LLM client

        Args:
            model: Ollama model name (e.g., 'gemma3:4b')
            host: Ollama host URL (optional, uses default if None)
            default_options: Default generation options
            timeout_s: Request timeout in seconds
            max_retries: Maximum retry attempts on failure
        """
        self.model = model
        self.host = host
        self.default_options = default_options or {}
        self.timeout_s = timeout_s
        self.max_retries = max_retries

    def generate(self, prompt: str, system: Optional[str] = None, options: Optional[Dict] = None) -> str:
        """
        Generate text using Ollama

        Args:
            prompt: The main prompt text
            system: Optional system message
            options: Optional generation parameters

        Returns:
            Generated text response
        """
        merged_options = {**self.default_options, **(options or {})}
        attempt = 0
        last_exc = None

        while attempt <= self.max_retries:
            try:
                kwargs = {
                    "model": self.model,
                    "prompt": prompt,
                    "options": merged_options
                }

                if system:
                    kwargs["system"] = system

                if self.host:
                    # Temporarily set OLLAMA_HOST environment variable
                    prev_host = os.environ.get("OLLAMA_HOST")
                    try:
                        os.environ["OLLAMA_HOST"] = self.host
                        resp = ollama.generate(**kwargs)
                    finally:
                        if prev_host is not None:
                            os.environ["OLLAMA_HOST"] = prev_host
                        else:
                            os.environ.pop("OLLAMA_HOST", None)
                else:
                    resp = ollama.generate(**kwargs)

                return resp.get("response", "")

            except Exception as e:
                last_exc = e
                logging.warning(f"Ollama generate failed (attempt {attempt+1}/{self.max_retries+1}): {e}")
                time.sleep(min(1.5 * (attempt + 1), 5))  # Exponential backoff
                attempt += 1

        raise RuntimeError(f"OllamaLLM failed after {self.max_retries+1} attempts") from last_exc
