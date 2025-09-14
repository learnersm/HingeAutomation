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

    def post_comment(self, comment: str, interaction_handler=None) -> bool:
        """
        Post a comment on the first photo of the current profile

        Args:
            comment: The comment text to post
            interaction_handler: Handler for UI interactions

        Returns:
            bool: True if comment posted successfully, False otherwise
        """
        handler = interaction_handler or self.interaction_handler
        if not handler:
            logging.error("No interaction handler provided for posting comment")
            return False

        if not comment or comment == 'N/A':
            logging.warning("No valid comment to post")
            return False

        try:
            # Validate comment length
            if not self.validate_comment(comment):
                logging.error(f"Comment too long: {len(comment)} characters")
                return False

            logging.info(f"Posting comment: '{comment}'")

            # Step 2: Click the heart/like icon to open comment box
            if not self._click_heart_icon(handler):
                logging.error("Failed to click heart icon")
                return False

            # Step 3: Type the comment
            if not self._type_comment(handler, comment):
                logging.error("Failed to type comment")
                return False

            # Step 4: Send the comment
            if not self._send_comment(handler):
                logging.error("Failed to send comment")
                return False

            logging.info("Comment posted successfully")
            return True

        except Exception as e:
            logging.error(f"Failed to post comment: {e}")
            return False

    

    def _click_heart_icon(self, handler) -> bool:
        """
        Click the heart/like icon to open comment box

        Args:
            handler: Interaction handler

        Returns:
            bool: True if clicked successfully
        """
        try:
            # Get heart button coordinates from UI detector
            from ui_detector import get_ui_detector
            ui_detector = get_ui_detector()
            heart_x, heart_y = ui_detector.get_heart_button_coords()
            logging.info(f"Using heart button coordinates: ({heart_x}, {heart_y})")

            # Take screenshot before clicking heart for comparison
            from screenshot_handler import ScreenshotHandler
            screenshot_handler = ScreenshotHandler()
            screenshot_handler.set_window_bounds(handler.window_bounds)
            before_heart_screenshot = screenshot_handler.capture_screenshot("before_heart_click.png")

            logging.info(f"Clicking heart icon at ({heart_x}, {heart_y})")
            success = handler.click_at(heart_x, heart_y)

            if success:
                # Wait for UI to respond
                time.sleep(1.0)

                # Take screenshot after clicking heart to check if screen changed
                after_heart_screenshot = screenshot_handler.capture_screenshot("after_heart_click.png")

                if before_heart_screenshot and after_heart_screenshot:
                    if screenshot_handler.compare_screenshots(before_heart_screenshot, after_heart_screenshot):
                        logging.warning("⚠️ ALERT: No screen content change detected after clicking heart/like icon!")
                        logging.warning("The heart icon click may have failed or the comment interface did not open")
                    else:
                        logging.info("Screen content changed after heart click - comment interface opened successfully")

                    # Clean up temporary screenshots
                    try:
                        import os
                        if os.path.exists(before_heart_screenshot):
                            os.remove(before_heart_screenshot)
                        if os.path.exists(after_heart_screenshot):
                            os.remove(after_heart_screenshot)
                    except Exception as e:
                        logging.debug(f"Could not clean up temporary screenshots: {e}")

            return success

        except Exception as e:
            logging.error(f"Failed to click heart icon: {e}")
            return False

    def _type_comment(self, handler, comment: str) -> bool:
        """
        Type the comment in the text box

        Args:
            handler: Interaction handler
            comment: Comment text to type

        Returns:
            bool: True if typed successfully
        """
        try:
            # Get comment box coordinates from UI detector
            from ui_detector import get_ui_detector
            ui_detector = get_ui_detector()

            # Get coordinates from UI detector
            text_box_x, text_box_y = ui_detector.get_comment_box_coords(handler.window_bounds)

            logging.info(f"Clicking comment text box at ({text_box_x}, {text_box_y})")
            handler.click_at(text_box_x, text_box_y)
            time.sleep(0.5)

            # Type the comment
            logging.info(f"Typing comment: {comment}")
            return handler.type_text(comment)

        except Exception as e:
            logging.error(f"Failed to type comment: {e}")
            return False

    # TODO : Later, wrong place for this method, 
    def _send_comment(self, handler) -> bool:
        """
        Send the comment by clicking send button

        Args:
            handler: Interaction handler

        Returns:
            bool: True if sent successfully
        """
        try:
            # Get send button coordinates from UI detector
            from ui_detector import get_ui_detector
            ui_detector = get_ui_detector()

            # Get coordinates from UI detector
            send_x, send_y = ui_detector.get_send_button_coords(handler.window_bounds)

            logging.info(f"Clicking send button at ({send_x}, {send_y})")
            time.sleep(0.5)
            success = handler.click_at(send_x, send_y)

            if success:
                time.sleep(1.0)  # Wait for comment to post
                logging.info("Comment sent successfully")

            return success

        except Exception as e:
            logging.error(f"Failed to send comment: {e}")
            return False

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

    def generate_fallback_comment(self, profile_data: Dict[str, Any]) -> str:
        """
        Generate a fallback comment if LLM fails

        Args:
            profile_data: Profile analysis data

        Returns:
            str: Fallback comment
        """
        fallback_comments = [
            "Hey! Your profile caught my attention 😊",
            "Love your vibe! What's your favorite hobby?",
            "You seem really interesting! Tell me more about yourself",
            "Great photos! What's the story behind them?",
        ]

        # Could be smarter based on profile_data, but keeping simple for now
        return fallback_comments[0]
