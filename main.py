"""
Hinge Automation Main Script
Orchestrates the overall automation workflow
"""

import logging
import sys
import os
import time

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from scrcpy_manager import ScrcpyManager
from window_detector import WindowDetector
from interaction_handler import InteractionHandler
from screenshot_handler import ScreenshotHandler
from profile_analyzer import ProfileAnalyzer
from comment_generator import CommentGenerator
from error_handler import ErrorHandler

def main():
    """
    Main automation workflow
    """
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Initialize components
    scrcpy_mgr = ScrcpyManager()
    window_detector = WindowDetector()
    interaction_handler = InteractionHandler()
    screenshot_handler = ScreenshotHandler()
    profile_analyzer = ProfileAnalyzer()
    comment_generator = CommentGenerator()
    error_handler = ErrorHandler()

    try:
        # Step 1: Run scrcpy in a terminal
        logging.info("Starting Hinge Automation - Step 1: Launching scrcpy")
        if not scrcpy_mgr.start_scrcpy():
            logging.error("Failed to start scrcpy. Exiting.")
            return

        logging.info("scrcpy launched successfully. Automation ready to proceed.")

        # Step 2: Identify the open window
        logging.info("Starting Hinge Automation - Step 2: Identifying the open window")
        if not window_detector.find_window():
            logging.error("Failed to find scrcpy window. Exiting.")
            return

        # Get window dimensions
        dimensions = window_detector.get_dimensions()
        if not dimensions:
            logging.error("Failed to get window dimensions. Exiting.")
            return

        logging.info("Window identified and dimensions obtained successfully.")

        # Placeholder for remaining steps
        # TODO: Implement steps 3-7 from project outline

    except Exception as e:
        logging.error(f"Main workflow error: {e}")
        error_handler.handle_error(e)
    finally:
        # Cleanup - stop scrcpy if running
        scrcpy_mgr.stop_scrcpy()
        error_handler.cleanup()

if __name__ == "__main__":
    main()
