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

from error_handler import ErrorHandler
from ui_detector import get_ui_detector
from config import TIMEOUTS

def like_and_post_comment(comment: str, interaction_handler, ui_detector, screenshot_handler) -> bool:
    """
    Like the profile and 
    Post a comment directly using interaction handler and UI detector

    Args:
        comment: The comment text to post
        interaction_handler: Handler for UI interactions
        ui_detector: UI detector for coordinates
        screenshot_handler: Handler for screenshots

    Returns:
        bool: True if comment posted successfully, False otherwise
    """
    if not comment or comment == 'N/A':
        logging.warning("No valid comment to post")
        return False

    try:
        # Step 1: Click the heart/like icon to open comment box
        heart_x, heart_y = ui_detector.get_heart_button_coords()
        logging.info(f"Clicking heart icon at ({heart_x}, {heart_y})")

        # Take screenshot before clicking heart for comparison
        before_heart_screenshot = screenshot_handler.capture_screenshot("before_heart_click.png")

        if not interaction_handler.click_at(heart_x, heart_y):
            logging.error("Failed to click heart icon")
            return False

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

        # Step 3: Type the comment
        text_box_x, text_box_y = ui_detector.get_comment_box_coords(interaction_handler.window_bounds)
        logging.info(f"Clicking comment text box at ({text_box_x}, {text_box_y})")
        interaction_handler.click_at(text_box_x, text_box_y)
        time.sleep(0.5)

        logging.info(f"Typing comment: {comment}")
        if not interaction_handler.type_text(comment):
            logging.error("Failed to type comment")
            return False

        # Step 4: Send the comment
        send_x, send_y = ui_detector.get_send_button_coords(interaction_handler.window_bounds)
        logging.info(f"Posting comment: '{comment}'")
        logging.info(f"Clicking send button at ({send_x}, {send_y})")
        time.sleep(0.5)

        if not interaction_handler.click_at(send_x, send_y):
            logging.error("Failed to send comment")
            return False

        # Wait for comment to post
        time.sleep(1.0)
        logging.info("Comment sent successfully")
        return True

    except Exception as e:
        logging.error(f"Failed to post comment: {e}")
        return False

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

    error_handler = ErrorHandler()
    ui_detector = get_ui_detector()

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

        # Quick analysis for pre-filtering
        print("\n" + "="*60)
        print("QUICK PROFILE ANALYSIS")
        print("="*60)
        logging.info("Performing quick analysis for profile filtering...")

        quick_result = profile_analyzer.quick_analyze_profile([first_screenshot])
        logging.info(f"Quick analysis result: Rating {quick_result['rating']}/10")
        logging.info(f"Red flags detected: {quick_result['has_red_flags']}")

        # Check if we should continue with full analysis
        if not profile_analyzer.should_continue_full_analysis(quick_result):
            logging.info("Profile filtered out by quick analysis - skipping to next profile")

            # Skip to next profile by clicking cross
            cross_x, cross_y = ui_detector.get_cross_button_coords()
            logging.info(f"Using cross button coordinates: ({cross_x}, {cross_y})")

            if interaction_handler.click_at(cross_x, cross_y):
                logging.info("Cross clicked - moving to next profile")
                # Wait for next profile to load
                time.sleep(TIMEOUTS["profile_load"])
            else:
                logging.error("Failed to click cross button")

            logging.info("Profile processing complete - quick filtered")
            return  # Exit early, don't continue with full analysis

        logging.info("Profile passed quick analysis - continuing with full screenshot capture")

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
            # Post the generated comment directly
            logging.info("Engaging with profile - posting comment")
            comment_success = like_and_post_comment(
                analysis_result['comment'],
                interaction_handler,
                ui_detector,
                screenshot_handler
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

            # TODO : Later : Refactor this code to a function
            # Take screenshot before clicking cross for comparison
            before_cross_screenshot = screenshot_handler.capture_screenshot("before_cross_click.png")

            # Get cross button coordinates from UI detector
            cross_x, cross_y = ui_detector.get_cross_button_coords()
            logging.info(f"Using cross button coordinates: ({cross_x}, {cross_y})")

            if interaction_handler.click_at(cross_x, cross_y):
                logging.info("Cross clicked - moving to next profile")

                # Wait a moment for UI to respond
                time.sleep(1.0)

                # Take screenshot after clicking cross to check if screen changed
                after_cross_screenshot = screenshot_handler.capture_screenshot("after_cross_click.png")

                if before_cross_screenshot and after_cross_screenshot:
                    if screenshot_handler.compare_screenshots(before_cross_screenshot, after_cross_screenshot):
                        logging.warning("⚠️ ALERT: No screen content change detected after clicking cross button!")
                        logging.warning("The cross button click may have failed or the UI did not respond as expected")
                    else:
                        logging.info("Screen content changed after cross click - navigation successful")

                    # Clean up temporary screenshots
                    try:
                        if os.path.exists(before_cross_screenshot):
                            os.remove(before_cross_screenshot)
                        if os.path.exists(after_cross_screenshot):
                            os.remove(after_cross_screenshot)
                    except Exception as e:
                        logging.debug(f"Could not clean up temporary screenshots: {e}")

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
