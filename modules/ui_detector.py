"""
UI Detector Module
Handles detection and location of UI elements like buttons on the screen
"""

import logging
from typing import Dict, Tuple, Optional
import pytesseract
from PIL import Image
from config import UI_TEXT_STRINGS

class UIDetector:
    """
    Detects and locates UI elements on the screen
    """

    def __init__(self):
        self.button_coordinates = {
            'cross': (810, 854),      # Cross button to skip profile
            'heart': (1107, 779),     # Heart/like button
            'comment_box': None,      # Comment text box (to be detected)
            'send_button': (1047,552),      # Send button (to be detected)
            'send_like_anyway': (984, 900)  # Send like anyway button, need on "send rose instead" intermediate screen
        }

    def find_button_coordinates(self, button_name: str) -> Optional[Tuple[int, int]]:
        """
        Find coordinates of a specific button

        Args:
            button_name: Name of the button ('cross', 'heart', etc.)

        Returns:
            Tuple of (x, y) coordinates or None if not found
        """
        if button_name in self.button_coordinates:
            coords = self.button_coordinates[button_name]
            if coords:
                logging.info(f"Found {button_name} button at coordinates: {coords}")
                return coords
            else:
                logging.warning(f"{button_name} button coordinates not available")
                return None
        else:
            logging.error(f"Unknown button name: {button_name}")
            return None

    def get_cross_button_coords(self) -> Tuple[int, int]:
        """
        Get coordinates of the cross button

        Returns:
            Tuple of (x, y) coordinates for cross button
        """
        coords = self.find_button_coordinates('cross')
        if coords:
            return coords
        else:
            # Fallback to default if detection fails
            logging.warning("Using fallback coordinates for cross button")
            return (810, 854)

    def get_heart_button_coords(self) -> Tuple[int, int]:
        """
        Get coordinates of the heart/like button

        Returns:
            Tuple of (x, y) coordinates for heart button
        """
        coords = self.find_button_coordinates('heart')
        if coords:
            return coords
        else:
            # Fallback to default if detection fails
            logging.warning("Using fallback coordinates for heart button")
            return (1107, 779)

    def get_comment_box_coords(self, window_bounds: Dict[str, int]) -> Tuple[int, int]:
        """
        Get coordinates of the comment text box

        Args:
            window_bounds: Window bounds dictionary with width/height

        Returns:
            Tuple of (x, y) coordinates for comment text box
        """
        coords = self.find_button_coordinates('comment_box')
        if coords and coords != (0, 0):
            return coords
        else:
            # Calculate coordinates: center horizontally, near bottom
            center_x = window_bounds['width'] // 2
            text_box_y = window_bounds['height'] * 4 // 5  # Near bottom
            logging.info(f"Calculated comment box coordinates: ({center_x}, {text_box_y})")
            return (center_x, text_box_y)

    def get_send_button_coords(self, window_bounds: Dict[str, int]) -> Tuple[int, int]:
        """
        Get coordinates of the send button

        Args:
            window_bounds: Window bounds dictionary with width/height

        Returns:
            Tuple of (x, y) coordinates for send button
        """
        coords = self.find_button_coordinates('send_button')
        if coords and coords != (0, 0):
            return coords
        else:
            # Fallback to default if detection fails
            logging.warning("Using fallback coordinates for heart button")
            return (1047, 552)

    def get_send_like_anyway_coords(self) -> Tuple[int, int]:
        """
        Get coordinates of the send like anyway button

        Returns:
            Tuple of (x, y) coordinates for send like anyway button
        """
        coords = self.find_button_coordinates('send_like_anyway')
        if coords:
            return coords
        else:
            # Fallback to default if detection fails
            logging.warning("Using fallback coordinates for send like anyway button")
            return (984, 900)

    def is_send_rose_screen(self, intermediate_screenshot: str) -> bool:
        """
        Check if the screenshot contains "send a rose instead" text using OCR

        Args:
            intermediate_screenshot: Path to the screenshot file to analyze

        Returns:
            bool: True if "send a rose instead" text is detected, False otherwise
        """
        try:
            # Open the image
            image = Image.open(intermediate_screenshot)

            # Perform OCR on the image
            ocr_text = pytesseract.image_to_string(image)

            # Log the OCR result for debugging
            logging.info(f"OCR text from screenshot: {ocr_text}")

            # Get the target text from config
            target_text = UI_TEXT_STRINGS.get("send_rose_instead", "send a rose instead")

            # Check if target text is present (case-insensitive)
            ocr_text_lower = ocr_text.lower()
            target_text_lower = target_text.lower()

            # Check for exact match or partial match
            if target_text_lower in ocr_text_lower:
                logging.info(f"✅ Found '{target_text}' in screenshot - this is a send rose screen")
                return True
            else:
                logging.info(f"❌ '{target_text}' not found in screenshot")
                return False

        except Exception as e:
            logging.error(f"Error performing OCR on screenshot {intermediate_screenshot}: {e}")
            # Return False on any error to avoid false positives
            return False
        
    
    

# Global instance for easy access
_ui_detector = None

def get_ui_detector():
    """
    Get the global UI detector instance

    Returns:
        UIDetector instance
    """
    global _ui_detector
    if _ui_detector is None:
        _ui_detector = UIDetector()
    return _ui_detector
