"""
Comment Generator Module
Handles witty comment creation and posting for Step 7
"""

import logging
import time
from typing import Dict, Any
from config import MAX_COMMENT_LENGTH
from modules.ai.ai_manager import get_llm

class CommentGenerator:
    def __init__(self, llm=None, interaction_handler=None):
        self.api_key = None  # For LLM API if used
        self.llm = llm or get_llm()
        self.interaction_handler = interaction_handler

    def validate_comment(self, comment: str) -> bool:
        """
        Validate comment length and content

        Args:
            comment: Comment to validate

        Returns:
            bool: True if valid
        """
        if not comment:
            return False

        if len(comment) > MAX_COMMENT_LENGTH:
            return False

        # Basic content validation (could be enhanced)
        if any(word in comment.lower() for word in ['spam', 'test', 'dummy']):
            return False

        return True

