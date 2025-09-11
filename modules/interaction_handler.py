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
            if self.window_bounds:
                # Convert relative coordinates to screen coordinates
                screen_x = self.window_bounds['left'] + x
                screen_y = self.window_bounds['top'] + y
            else:
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
            pyautogui.dragTo(end_screen_x, end_screen_y, duration=duration)
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

    def wait_for_interaction(self):
        """
        Wait for interaction to complete
        """
        time.sleep(TIMEOUTS["interaction_delay"])

    def find_and_click_app(self, app_name="Hinge"):
        """
        Find and click on an app by name using OCR
        """
        if not PYAUTOGUI_AVAILABLE:
            logging.error("pyautogui not available. Cannot find app.")
            return False

        try:
            # Take a screenshot to analyze
            screenshot = pyautogui.screenshot()
            if self.window_bounds:
                # Crop to window region
                screenshot = screenshot.crop((
                    self.window_bounds['left'],
                    self.window_bounds['top'],
                    self.window_bounds['right'],
                    self.window_bounds['bottom']
                ))

            # Use OCR to find the app name
            try:
                import pytesseract
                from PIL import Image
                text_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

                for i, word in enumerate(text_data['text']):
                    if app_name.lower() in word.lower():
                        # Found the app name, get its position
                        x = text_data['left'][i] + text_data['width'][i] // 2
                        y = text_data['top'][i] + text_data['height'][i] // 2

                        # Convert to screen coordinates if window bounds are set
                        if self.window_bounds:
                            x += self.window_bounds['left']
                            y += self.window_bounds['top']

                        logging.info(f"Found '{app_name}' at ({x}, {y}), clicking...")
                        return self.click_at(x, y)

            except ImportError:
                logging.warning("pytesseract not available. Cannot use OCR to find app.")

            # Fallback: Try to locate common app positions (grid layout)
            # This is a simple heuristic for Android home screen
            if self.window_bounds:
                width = self.window_bounds['width']
                height = self.window_bounds['height']

                # Try clicking in the center first (common position for main apps)
                center_x = width // 2
                center_y = height // 2
                logging.info(f"Trying to click at center: ({center_x}, {center_y})")
                if self.click_at(center_x, center_y):
                    time.sleep(2)  # Wait to see if app opens
                    return True

                # Try other common positions in a grid
                grid_positions = [
                    (width // 4, height // 4),
                    (3 * width // 4, height // 4),
                    (width // 4, 3 * height // 4),
                    (3 * width // 4, 3 * height // 4),
                    (width // 2, height // 3),
                    (width // 2, 2 * height // 3)
                ]

                for pos_x, pos_y in grid_positions:
                    logging.info(f"Trying to click at grid position: ({pos_x}, {pos_y})")
                    if self.click_at(pos_x, pos_y):
                        time.sleep(2)
                        # Check if Hinge opened by taking another screenshot and checking for Hinge UI elements
                        # For now, just return True assuming it worked
                        return True

            logging.error(f"Could not find and click on {app_name} app")
            return False

        except Exception as e:
            logging.error(f"Error finding and clicking app: {e}")
            return False
