"""
Window Detector Module
Handles window identification and dimension analysis
"""

import logging
import time
from config import WINDOW_TITLE, TIMEOUTS

try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False
    logging.warning("pygetwindow not available. Window detection will be limited.")

class WindowDetector:
    def __init__(self):
        self.window = None
        self.dimensions = None

    def find_window(self):
        """
        Locate the scrcpy window by title
        """
        if not PYGETWINDOW_AVAILABLE:
            logging.error("pygetwindow not installed. Cannot detect windows.")
            return False

        try:
            logging.info(f"Searching for window with title: {WINDOW_TITLE}")

            # Debug: List all available windows
            try:
                all_titles = gw.getAllTitles()
                logging.info(f"Available window titles: {all_titles[:10]}...")  # Show first 10
            except Exception as e:
                logging.warning(f"Could not list window titles: {e}")

            # Wait for window to appear
            max_attempts = int(TIMEOUTS["window_detection"] / 0.5)
            for attempt in range(max_attempts):
                # Try different pygetwindow methods
                try:
                    # Method 1: getAllTitles and getWindowByTitle
                    titles = gw.getAllTitles()
                    if WINDOW_TITLE in titles:
                        self.window = gw.getWindowByTitle(WINDOW_TITLE)
                        logging.info(f"Found window: {self.window.title}")
                        return True
                except:
                    pass

                try:
                    # Method 2: getWindowsWithTitle (if available)
                    windows = gw.getWindowsWithTitle(WINDOW_TITLE)
                    if windows:
                        self.window = windows[0]
                        logging.info(f"Found window: {self.window.title}")
                        return True
                except:
                    pass

                # Check for scrcpy in all available titles
                try:
                    titles = gw.getAllTitles()
                    for title in titles:
                        if title and "scrcpy" in title.lower():
                            logging.info(f"Found scrcpy in titles: '{title}'")
                            try:
                                self.window = gw.getWindowByTitle(title)
                                logging.info(f"Successfully got window object: {self.window.title}")
                                return True
                            except Exception as e:
                                logging.warning(f"Could not get window object for title '{title}': {e}")
                except Exception as e:
                    logging.warning(f"Error checking titles: {e}")

                time.sleep(0.5)

            logging.error(f"Window with title '{WINDOW_TITLE}' not found after {TIMEOUTS['window_detection']} seconds")
            return False

        except Exception as e:
            logging.error(f"Error finding window: {e}")
            return False

    def get_dimensions(self):
        """
        Get window dimensions and position
        """
        if not self.window:
            logging.error("No window found. Call find_window() first.")
            return None

        try:
            dimensions = {
                'left': self.window.left,
                'top': self.window.top,
                'width': self.window.width,
                'height': self.window.height,
                'right': self.window.right,
                'bottom': self.window.bottom
            }
            self.dimensions = dimensions
            logging.info(f"Window dimensions: {dimensions}")
            return dimensions

        except Exception as e:
            logging.error(f"Error getting window dimensions: {e}")
            return None

    def is_window_active(self):
        """
        Check if window is active and visible
        """
        if not self.window:
            return False

        try:
            return self.window.isActive and self.window.visible
        except Exception as e:
            logging.error(f"Error checking window status: {e}")
            return False

    def get_active_window(self):
        """
        Get the currently active window
        """
        if not PYGETWINDOW_AVAILABLE:
            logging.error("pygetwindow not installed. Cannot detect active window.")
            return False

        try:
            # For macOS, getActiveWindow() returns a string (title), not a window object
            active_title = gw.getActiveWindow()
            if active_title:
                logging.info(f"Active window title: {active_title}")

                # Create a simple window-like object with the title and geometry
                # Since macOS implementation is incomplete, we'll work with what we have
                geometry = gw.getWindowGeometry(active_title)
                if geometry:
                    left, top, width, height = geometry
                    logging.info(f"Raw window geometry: left={left}, top={top}, width={width}, height={height}")

                    # On macOS, sometimes the geometry includes window decorations
                    # Let's try to get a more accurate region by checking all windows
                    try:
                        all_windows = gw.getAllWindows()
                        for win in all_windows:
                            if win.title == active_title:
                                # Use the actual window object if available
                                left, top, width, height = win.left, win.top, win.width, win.height
                                logging.info(f"Using window object geometry: left={left}, top={top}, width={width}, height={height}")
                                break
                    except Exception as e:
                        logging.warning(f"Could not get window object geometry, using getWindowGeometry: {e}")

                    # Create a simple object to hold window properties
                    class SimpleWindow:
                        def __init__(self, title, left, top, width, height):
                            self.title = title
                            self.left = left
                            self.top = top
                            self.width = width
                            self.height = height
                            self.right = left + width
                            self.bottom = top + height
                            self.isActive = True
                            self.visible = True

                    self.window = SimpleWindow(active_title, left, top, width, height)
                    logging.info(f"Active window object created: {self.window.title}")
                    logging.info(f"Final window bounds: left={left}, top={top}, width={width}, height={height}")
                    return True
                else:
                    logging.error("Could not get window geometry")
                    return False
            else:
                logging.error("No active window found")
                return False
        except Exception as e:
            logging.error(f"Error getting active window: {e}")
            return False

    def activate_window(self):
        """
        Bring window to foreground
        """
        if not self.window:
            logging.error("No window found. Call find_window() first.")
            return False

        try:
            self.window.activate()
            logging.info("Window activated")
            return True
        except Exception as e:
            logging.error(f"Error activating window: {e}")
            return False
