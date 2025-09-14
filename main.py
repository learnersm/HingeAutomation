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

def cleanup_screenshots():
    """
    Clean up screenshot directories before each run
    - Clear screenshots_from_last_run folder
    - Move all images from screenshots folder to screenshots_from_last_run
    - Clear the screenshots folder
    """
    import shutil

    screenshots_dir = "screenshots"
    last_run_dir = "screenshots_from_last_run"

    try:
        # Create directories if they don't exist
        os.makedirs(screenshots_dir, exist_ok=True)
        os.makedirs(last_run_dir, exist_ok=True)

        # Clear screenshots_from_last_run folder
        for filename in os.listdir(last_run_dir):
            file_path = os.path.join(last_run_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Removed old file from last run: {filename}")

        # Move all files from screenshots to screenshots_from_last_run
        for filename in os.listdir(screenshots_dir):
            src_path = os.path.join(screenshots_dir, filename)
            dst_path = os.path.join(last_run_dir, filename)
            if os.path.isfile(src_path):
                shutil.move(src_path, dst_path)
                logging.info(f"Moved screenshot to last run: {filename}")

        # Clear the screenshots folder (should be empty now, but just in case)
        for filename in os.listdir(screenshots_dir):
            file_path = os.path.join(screenshots_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Cleaned up remaining file: {filename}")

        logging.info("Screenshot cleanup completed successfully")

    except Exception as e:
        logging.error(f"Error during screenshot cleanup: {e}")

def main():
    """
    Main automation workflow
    """
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Clean up screenshots from previous run
    logging.info("Performing screenshot cleanup from previous run...")
    cleanup_screenshots()

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

        # Step 2: Identify the active window and prepare Hinge app
        print("\n" + "="*60)
        print("STEP 2: WINDOW & APP PREPARATION")
        print("="*60)
        print("Please do BOTH of the following within 10 seconds:")
        print("1. Make the scrcpy window ACTIVE (click on it)")
        print("2. Open the Hinge app on your device")
        print("="*60)

        # Wait 10 seconds for user to activate window and open Hinge app
        for i in range(10, 0, -1):
            print(f"\rTime remaining: {i} seconds", end="", flush=True)
            time.sleep(1)
        print("\rPreparation time complete!     ")

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

        logging.info("Window and Hinge app preparation complete")
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
        consecutive_identical = 0  # Track consecutive identical screenshots
        max_identical_threshold = 2  # Stop after 2 identical screenshots

        while scroll_count < max_scrolls:
            # Perform full swipe (almost end to end screen)
            start_y = dimensions['height'] * 9 // 10  # Near bottom
            end_y = dimensions['height'] // 10       # Near top
            center_x = dimensions['width'] // 2

            logging.info(f"Performing full scroll {scroll_count + 1}")
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

            # Check if screenshot is different from the last one (end of profile detection)
            if len(profile_screenshots) > 0:
                last_screenshot = profile_screenshots[-1]
                if screenshot_handler.compare_screenshots(last_screenshot, new_screenshot):
                    consecutive_identical += 1
                    logging.info(f"Screenshots are identical (count: {consecutive_identical}/{max_identical_threshold})")

                    # If we've seen identical screenshots multiple times, we've reached the end
                    if consecutive_identical >= max_identical_threshold:
                        logging.info("Reached end of profile - stopping scroll")
                        # Remove the identical screenshot
                        os.remove(new_screenshot)
                        break
                    else:
                        # Keep the screenshot but continue (might be temporary UI state)
                        profile_screenshots.append(new_screenshot)
                        logging.info(f"Screenshot captured (may be duplicate): {new_screenshot}")
                else:
                    # Reset counter when we get different content
                    consecutive_identical = 0
                    profile_screenshots.append(new_screenshot)
                    logging.info(f"New screenshot captured: {new_screenshot}")
            else:
                # First scroll screenshot
                profile_screenshots.append(new_screenshot)
                logging.info(f"New screenshot captured: {new_screenshot}")

            scroll_count += 1

        logging.info(f"Profile screenshot capture complete. Total screenshots: {len(profile_screenshots)}")
        for screenshot in profile_screenshots:
            logging.info(f"Profile screenshot: {screenshot}")

        # Remove the last screenshot if it's a duplicate (end of profile detection)
        if len(profile_screenshots) > 1:
            last_screenshot = profile_screenshots[-1]
            second_last_screenshot = profile_screenshots[-2]

            if screenshot_handler.compare_screenshots(second_last_screenshot, last_screenshot):
                logging.info("Removing duplicate last screenshot before AI analysis")
                # Remove the duplicate screenshot from the list
                removed_screenshot = profile_screenshots.pop()
                # Also remove the file from disk
                if os.path.exists(removed_screenshot):
                    os.remove(removed_screenshot)
                    logging.info(f"Removed duplicate screenshot file: {removed_screenshot}")

        logging.info(f"Final screenshots for AI analysis: {len(profile_screenshots)}")
        for screenshot in profile_screenshots:
            logging.info(f"Analysis screenshot: {screenshot}")

        # Step 7: Analyze profile and decide action
        print("\n" + "="*60)
        print("STEP 7: PROFILE ANALYSIS & ENGAGEMENT")
        print("="*60)

        # Analyze the profile using vision LLM
        logging.info("Analyzing profile with AI...")
        analysis_result = profile_analyzer.analyze_profile(profile_screenshots)

        logging.info(f"Analysis result: Rating {analysis_result['rating']}/10, Decision: {analysis_result['decision']}")
        logging.info(f"Reason: {analysis_result['reason']}")

        # Make decision based on analysis
        if profile_analyzer.should_engage_profile(analysis_result):
            # Post the generated comment
            logging.info("Engaging with profile - posting comment")
            comment_success = comment_generator.post_comment(
                analysis_result['comment'],
                interaction_handler
            )

            if comment_success:
                logging.info("Comment posted successfully - waiting for next profile")
                # Wait for next profile to load
                time.sleep(TIMEOUTS["profile_load"])
            else:
                logging.error("Failed to post comment")
                # Could implement retry logic here
        else:
            # Skip to next profile by clicking cross
            logging.info("Skipping profile - clicking cross")
            # Assume cross button is at top right of profile
            cross_x = dimensions['width'] * 9 // 10  # Right side
            cross_y = dimensions['height'] // 10     # Top area

            if interaction_handler.click_at(cross_x, cross_y):
                logging.info("Cross clicked - moving to next profile")
                # Wait for next profile to load
                time.sleep(TIMEOUTS["profile_load"])
            else:
                logging.error("Failed to click cross button")

        # Continue the loop for next profile
        # In a real implementation, this would be in a loop
        logging.info("Profile processing complete - ready for next profile")

    except Exception as e:
        logging.error(f"Main workflow error: {e}")
        error_handler.handle_error(e)
    finally:
        # Cleanup - stop scrcpy if running
        scrcpy_mgr.stop_scrcpy()
        error_handler.cleanup()

if __name__ == "__main__":
    main()
