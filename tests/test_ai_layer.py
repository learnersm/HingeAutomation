#!/usr/bin/env python3
"""
Test script for AI layer
Verifies that the Ollama integration works as expected
"""

import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from ai import get_llm

def test_ai_layer():
    """
    Test the AI layer with a simple prompt
    """
    print("Testing AI Layer with Ollama...")

    try:
        # Get configured LLM instance
        llm = get_llm()
        print(f"LLM instance created: {type(llm).__name__}")

        # Test with the user's working prompt
        prompt = "Tell me a 1 liner short story about a talking cat. Limit to 50 words"
        print(f"Prompt: {prompt}")

        response = llm.generate(prompt)
        print(f"Response: {response}")

        print("✅ AI layer test successful!")

    except Exception as e:
        print(f"❌ AI layer test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_ai_layer()
    sys.exit(0 if success else 1)
