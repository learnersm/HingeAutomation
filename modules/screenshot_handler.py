"""
Screenshot Handler Module
Handles screenshot capture and management
"""

import os
import logging
import time
from datetime import datetime
from config import SCREENSHOT_DIR, SCREENSHOT_FORMAT, TIMEOUTS

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logging.warning("pyautogui not available. Screenshot capture will be limited.")

try:
    from PIL import Image, ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL not available. Image processing will be limited.")

class ScreenshotHandler:
    def __init__(self):
        self.screenshot_dir = SCREENSHOT_DIR
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.window_bounds = None

    def set_window_bounds(self, bounds):
        """
        Set the window bounds for screenshot region
        """
        self.window_bounds = bounds

    def capture_screenshot(self, filename=None):
        """
        Capture screenshot of the window or full screen using pygetwindow + ImageGrab
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.{SCREENSHOT_FORMAT}"

            filepath = os.path.join(self.screenshot_dir, filename)

            if self.window_bounds:
                # Use pygetwindow + ImageGrab approach as suggested
                try:
                    import pygetwindow as gw

                    # Get the active window title from our window bounds
                    # Since we have the bounds, let's try to find the window by position
                    left = int(self.window_bounds['left'])
                    top = int(self.window_bounds['top'])
                    width = int(self.window_bounds['width'])
                    height = int(self.window_bounds['height'])

                    logging.info(f"Capturing screenshot of region: ({left}, {top}, {width}, {height})")

                    # Try to find the window at these coordinates
                    try:
                        windows = gw.getAllWindows()
                        target_window = None

                        for win in windows:
                            # Check if window bounds match our target region
                            if (abs(win.left - left) < 10 and  # Allow small tolerance
                                abs(win.top - top) < 10 and
                                abs(win.width - width) < 10 and
                                abs(win.height - height) < 10):
                                target_window = win
                                logging.info(f"Found matching window: {win.title}")
                                break

                        # If we found a matching window, activate it first
                        if target_window:
                            target_window.activate()
                            time.sleep(0.5)  # Wait for activation

                    except Exception as e:
                        logging.warning(f"Could not find/activate window: {e}")

                    # Take screenshot using ImageGrab (more reliable than pyautogui on macOS)
                    if PIL_AVAILABLE:
                        # Use ImageGrab.grab() with bbox parameter for region capture
                        bbox = (left, top, left + width, top + height)
                        screenshot = ImageGrab.grab(bbox=bbox)
                        logging.info(f"Captured screenshot size: {screenshot.size}")

                        # Save the screenshot
                        screenshot.save(filepath)
                        logging.info(f"Screenshot saved to: {filepath}")
                        return filepath
                    else:
                        logging.error("PIL not available. Cannot capture screenshot.")
                        return None

                except ImportError:
                    logging.warning("pygetwindow not available, falling back to pyautogui")

                # Fallback to pyautogui if pygetwindow approach fails
                if PYAUTOGUI_AVAILABLE:
                    logging.info("Falling back to pyautogui")
                    left = int(self.window_bounds['left'])
                    top = int(self.window_bounds['top'])
                    width = int(self.window_bounds['width'])
                    height = int(self.window_bounds['height'])

                    region = (left, top, width, height)
                    screenshot = pyautogui.screenshot(region=region)
                    logging.info(f"Captured screenshot size: {screenshot.size}")

                    if PIL_AVAILABLE:
                        screenshot.save(filepath)
                        logging.info(f"Screenshot saved with pyautogui: {filepath}")
                        return filepath
                else:
                    logging.error("No screenshot method available.")
                    return None
            else:
                # Capture full screen
                logging.info("Capturing full screen screenshot")
                if PIL_AVAILABLE:
                    screenshot = ImageGrab.grab()
                    screenshot.save(filepath)
                    logging.info(f"Full screenshot saved to: {filepath}")
                    return filepath
                elif PYAUTOGUI_AVAILABLE:
                    screenshot = pyautogui.screenshot()
                    if PIL_AVAILABLE:
                        screenshot.save(filepath)
                        logging.info(f"Full screenshot saved to: {filepath}")
                        return filepath
                else:
                    logging.error("No screenshot method available.")
                    return None

        except Exception as e:
            logging.error(f"Error capturing screenshot: {e}")
            return None

    def save_screenshot(self, image, filename):
        """
        Save screenshot to file
        """
        if not PIL_AVAILABLE:
            logging.error("PIL not available. Cannot save screenshot.")
            return False

        try:
            filepath = os.path.join(self.screenshot_dir, filename)
            image.save(filepath)
            logging.info(f"Screenshot saved to: {filepath}")
            return True
        except Exception as e:
            logging.error(f"Error saving screenshot: {e}")
            return False

    def get_latest_screenshot(self):
        """
        Get the most recent screenshot
        """
        try:
            files = [f for f in os.listdir(self.screenshot_dir) if f.endswith(f".{SCREENSHOT_FORMAT}")]
            if not files:
                return None

            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.screenshot_dir, x)), reverse=True)
            latest_file = os.path.join(self.screenshot_dir, files[0])
            logging.info(f"Latest screenshot: {latest_file}")
            return latest_file
        except Exception as e:
            logging.error(f"Error getting latest screenshot: {e}")
            return None

    def cleanup_old_screenshots(self, keep_recent=10):
        """
        Remove old screenshot files, keeping the most recent ones
        """
        try:
            files = [f for f in os.listdir(self.screenshot_dir) if f.endswith(f".{SCREENSHOT_FORMAT}")]
            if len(files) <= keep_recent:
                return

            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.screenshot_dir, x)))
            files_to_delete = files[:-keep_recent]

            for file in files_to_delete:
                filepath = os.path.join(self.screenshot_dir, file)
                os.remove(filepath)
                logging.info(f"Deleted old screenshot: {filepath}")

        except Exception as e:
            logging.error(f"Error cleaning up screenshots: {e}")

    def compare_screenshots(self, screenshot1_path, screenshot2_path):
        """
        Compare two screenshots to check if they are identical
        Returns True if identical, False otherwise
        """
        if not PIL_AVAILABLE:
            logging.error("PIL not available. Cannot compare screenshots.")
            return False

        try:
            img1 = Image.open(screenshot1_path)
            img2 = Image.open(screenshot2_path)

            # Check if images are identical
            if img1.size != img2.size:
                return False

            # Compare pixel by pixel
            diff = Image.new("RGB", img1.size)
            diff_pixels = []
            for x in range(img1.width):
                for y in range(img1.height):
                    if img1.getpixel((x, y)) != img2.getpixel((x, y)):
                        diff_pixels.append((x, y))

            # If less than 1% of pixels differ, consider identical
            total_pixels = img1.width * img1.height
            diff_percentage = len(diff_pixels) / total_pixels
            is_identical = diff_percentage < 0.01

            logging.info(f"Screenshot comparison: {diff_percentage:.2%} difference, identical: {is_identical}")
            return is_identical

        except Exception as e:
            logging.error(f"Error comparing screenshots: {e}")
            return False
