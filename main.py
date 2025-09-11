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
from config import TIMEOUTS

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

        # Step 2: Identify the active window
        print("\n" + "="*60)
        print("STEP 2: WINDOW IDENTIFICATION")
        print("="*60)
        print("Please make the scrcpy window ACTIVE (click on it)")
        print("You have 5 seconds...")
        print("="*60)

        # Wait 5 seconds for user to activate the window
        for i in range(5, 0, -1):
            print(f"\rTime remaining: {i} seconds", end="", flush=True)
            time.sleep(1)
        print("\rWindow activation time complete!     ")

        # Get the active window
        logging.info("Detecting active window...")
        if not window_detector.get_active_window():
            logging.error("Failed to get active window. Exiting.")
            return

        # Get window dimensions
        dimensions = window_detector.get_dimensions()
        if not dimensions:
            logging.error("Failed to get window dimensions. Exiting.")
            return

        logging.info("Active window identified and dimensions obtained successfully.")
        print(f"Window dimensions: {dimensions['width']}x{dimensions['height']} at ({dimensions['left']}, {dimensions['top']})")

        # Set window bounds for handlers
        interaction_handler.set_window_bounds(dimensions)
        screenshot_handler.set_window_bounds(dimensions)

        # Step 4: Open the Hinge app manually
        print("\n" + "="*60)
        print("STEP 4: OPENING HINGE APP")
        print("="*60)
        print("Please manually open the Hinge app on your device:")
        print("1. Look at the scrcpy window showing your Android device")
        print("2. Find and tap the Hinge app icon")
        print("3. Wait for the Hinge app to fully load")
        print("4. Press Enter here when ready to continue...")

        input("Press Enter to continue with automation...")
        logging.info("User confirmed Hinge app is open")
        print("Continuing with automation...")

        # Step 5: Wait for first profile to load
        print("\n" + "="*60)
        print("STEP 5: WAITING FOR PROFILE TO LOAD")
        print("="*60)
        logging.info("Waiting for profile to load...")
        time.sleep(TIMEOUTS["profile_load"])
        logging.info("Profile load wait complete")

        # Step 6: Take screenshots of profile with scrolling
        print("\n" + "="*60)
        print("STEP 6: CAPTURING PROFILE SCREENSHOTS")
        print("="*60)

        profile_screenshots = []

        # Take first screenshot
        logging.info("Taking first profile screenshot")
        first_screenshot = screenshot_handler.capture_screenshot("profile_001.png")
        if first_screenshot:
            profile_screenshots.append(first_screenshot)
            logging.info(f"First screenshot captured: {first_screenshot}")
        else:
            logging.error("Failed to capture first screenshot")
            return

        # Scroll and take more screenshots
        max_scrolls = 10  # Prevent infinite loop
        scroll_count = 0
        previous_screenshot = first_screenshot

        while scroll_count < max_scrolls:
            # Perform scroll (swipe up to scroll down)
            start_y = dimensions['height'] * 3 // 4
            end_y = dimensions['height'] // 4
            center_x = dimensions['width'] // 2

            logging.info(f"Performing scroll {scroll_count + 1}")
            if not interaction_handler.swipe(center_x, start_y, center_x, end_y):
                logging.error("Failed to perform scroll")
                break

            # Wait for scroll to complete
            time.sleep(TIMEOUTS["scroll_wait"])

            # Take new screenshot
            screenshot_num = len(profile_screenshots) + 1
            new_screenshot = screenshot_handler.capture_screenshot(f"profile_{screenshot_num:03d}.png")

            if not new_screenshot:
                logging.error("Failed to capture screenshot after scroll")
                break

            # Check if screenshot is different (new content)
            if screenshot_handler.compare_screenshots(previous_screenshot, new_screenshot):
                logging.info("Screenshots are identical, reached end of profile")
                # Remove the identical screenshot
                os.remove(new_screenshot)
                break
            else:
                profile_screenshots.append(new_screenshot)
                previous_screenshot = new_screenshot
                logging.info(f"New screenshot captured: {new_screenshot}")

            scroll_count += 1

        logging.info(f"Profile screenshot capture complete. Total screenshots: {len(profile_screenshots)}")
        for screenshot in profile_screenshots:
            logging.info(f"Profile screenshot: {screenshot}")

        # Placeholder for remaining steps
        # TODO: Implement steps 7 from project outline

    except Exception as e:
        logging.error(f"Main workflow error: {e}")
        error_handler.handle_error(e)
    finally:
        # Cleanup - stop scrcpy if running
        scrcpy_mgr.stop_scrcpy()
        error_handler.cleanup()

if __name__ == "__main__":
    main()
