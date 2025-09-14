"""
Interaction Handler Module
Handles GUI interactions (clicks, swipes, typing)
"""

import logging
import time
from config import TIMEOUTS

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logging.warning("pyautogui not available. GUI interactions will be limited.")

class InteractionHandler:
    def __init__(self):
        self.window_bounds = None
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = TIMEOUTS["interaction_delay"]

    def set_window_bounds(self, bounds):
        """
        Set the window bounds for coordinate translation
        """
        self.window_bounds = bounds

    def click_at(self, x, y):
        """
        Click at specified coordinates (relative to window)
        """
        if not PYAUTOGUI_AVAILABLE:
            logging.error("pyautogui not available. Cannot perform click.")
            return False

        try:
            # TODO : Later : Add a coordinate genarator layer, , Interaction handler works with coordinates as is, does not manupulate them
            # if self.window_bounds:
            #     # Convert relative coordinates to screen coordinates
            #     screen_x = self.window_bounds['left'] + x
            #     screen_y = self.window_bounds['top'] + y
            # else:
            screen_x, screen_y = x, y

            logging.info(f"Clicking at screen coordinates: ({screen_x}, {screen_y})")
            pyautogui.click(screen_x, screen_y)
            time.sleep(TIMEOUTS["interaction_delay"])
            return True
        except Exception as e:
            logging.error(f"Error clicking at ({x}, {y}): {e}")
            return False

    def swipe(self, start_x, start_y, end_x, end_y, duration=0.5):
        """
        Perform swipe gesture from start to end coordinates
        """
        if not PYAUTOGUI_AVAILABLE:
            logging.error("pyautogui not available. Cannot perform swipe.")
            return False

        try:
            if self.window_bounds:
                # Convert relative coordinates to screen coordinates
                start_screen_x = self.window_bounds['left'] + start_x
                start_screen_y = self.window_bounds['top'] + start_y
                end_screen_x = self.window_bounds['left'] + end_x
                end_screen_y = self.window_bounds['top'] + end_y
            else:
                start_screen_x, start_screen_y = start_x, start_y
                end_screen_x, end_screen_y = end_x, end_y

            logging.info(f"Swiping from ({start_screen_x}, {start_screen_y}) to ({end_screen_x}, {end_screen_y})")
            pyautogui.moveTo(start_screen_x, start_screen_y)
            pyautogui.dragTo(end_screen_x, end_screen_y, duration=duration, button='left')
            time.sleep(TIMEOUTS["interaction_delay"])
            return True
        except Exception as e:
            logging.error(f"Error swiping: {e}")
            return False

    def type_text(self, text):
        """
        Type text input
        """
        if not PYAUTOGUI_AVAILABLE:
            logging.error("pyautogui not available. Cannot type text.")
            return False

        try:
            logging.info(f"Typing text: {text}")
            pyautogui.typewrite(text)
            time.sleep(TIMEOUTS["interaction_delay"])
            return True
        except Exception as e:
            logging.error(f"Error typing text: {e}")
            return False
