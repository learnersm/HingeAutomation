"""
UI Detector Module
Handles detection and location of UI elements like buttons on the screen
"""

import logging
from typing import Dict, Tuple, Optional

class UIDetector:
    """
    Detects and locates UI elements on the screen
    """

    def __init__(self):
        self.button_coordinates = {
            'cross': (810, 854),      # Cross button to skip profile
            'heart': (1107, 779),     # Heart/like button
            'comment_box': None,      # Comment text box (to be detected)
            'send_button': (1047,552)       # Send button (to be detected)
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
