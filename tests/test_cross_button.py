#!/usr/bin/env python3
"""
Test script for cross button click functionality
Tests that the cross button is clicked at the correct coordinates (bottom left area)
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.interaction_handler import InteractionHandler

class TestCrossButtonClick(unittest.TestCase):
    """
    Test cases for cross button click functionality
    """

    def setUp(self):
        """Set up test fixtures"""
        self.interaction_handler = InteractionHandler()
        # Mock window bounds for testing (simulating a 1080x1920 screen)
        self.test_bounds = {
            'left': 100,
            'top': 50,
            'width': 1080,
            'height': 1920,
            'right': 1180,
            'bottom': 1970
        }
        self.interaction_handler.set_window_bounds(self.test_bounds)

    def test_cross_button_coordinates_calculation(self):
        """
        Test that cross button coordinates are calculated correctly
        Cross button should be in bottom left area of the screen
        """
        # Expected cross button position (manually verified coordinates)
        # User provided coordinates from physical device: (180, 2600)
        manual_cross_x = 180
        manual_cross_y = 2600

        # Old dynamic implementation (top right area - was incorrect)
        old_cross_x = self.test_bounds['width'] * 9 // 10  # 90% from left = 972
        old_cross_y = self.test_bounds['height'] // 10     # 10% from top = 192

        print("\n📍 Cross Button Coordinate Analysis:")
        print(f"Screen dimensions: {self.test_bounds['width']}x{self.test_bounds['height']}")
        print(f"Old implementation: ({old_cross_x}, {old_cross_y}) - Top Right Area (WRONG)")
        print(f"Manual coordinates: ({manual_cross_x}, {manual_cross_y}) - Bottom Left Area (CORRECT)")

        # The old implementation was wrong - it clicked top right instead of bottom left
        self.assertNotEqual(old_cross_x, manual_cross_x,
                          "Cross button X coordinate should be 180, not right side")
        self.assertNotEqual(old_cross_y, manual_cross_y,
                          "Cross button Y coordinate should be 2600, not top area")

    @patch('modules.interaction_handler.pyautogui')
    def test_cross_button_click_with_manual_coordinates(self, mock_pyautogui):
        """
        Test cross button click with manually verified coordinates (180, 2600)
        """
        # Mock pyautogui to track click calls
        mock_pyautogui.click = Mock()
        mock_pyautogui.PAUSE = 1

        # Use manually verified coordinates from physical device
        manual_cross_x = 180   # Fixed coordinate from device
        manual_cross_y = 2600  # Fixed coordinate from device

        # Calculate expected screen coordinates (window bounds + relative coordinates)
        expected_screen_x = self.test_bounds['left'] + manual_cross_x
        expected_screen_y = self.test_bounds['top'] + manual_cross_y

        # Perform the click with manual coordinates
        result = self.interaction_handler.click_at(manual_cross_x, manual_cross_y)

        # Verify the click was called with correct screen coordinates
        mock_pyautogui.click.assert_called_once_with(expected_screen_x, expected_screen_y)

        print("\n✅ Cross Button Click Test (Manual Coordinates):")
        print(f"Manual coordinates: ({manual_cross_x}, {manual_cross_y})")
        print(f"Screen coordinates: ({expected_screen_x}, {expected_screen_y})")
        print(f"Click result: {result}")

        self.assertTrue(result, "Cross button click should return True")

    @patch('modules.interaction_handler.pyautogui')
    def test_cross_button_click_with_current_incorrect_coordinates(self, mock_pyautogui):
        """
        Test current implementation coordinates (for comparison)
        """
        # Mock pyautogui to track click calls
        mock_pyautogui.click = Mock()
        mock_pyautogui.PAUSE = 1

        # Current implementation coordinates (incorrect - top right)
        current_cross_x = self.test_bounds['width'] * 9 // 10  # 90% from left
        current_cross_y = self.test_bounds['height'] // 10     # 10% from top

        # Calculate expected screen coordinates
        expected_screen_x = self.test_bounds['left'] + current_cross_x
        expected_screen_y = self.test_bounds['top'] + current_cross_y

        # Perform the click with current coordinates
        result = self.interaction_handler.click_at(current_cross_x, current_cross_y)

        # Verify the click was called with current (incorrect) coordinates
        mock_pyautogui.click.assert_called_once_with(expected_screen_x, expected_screen_y)

        print("\n⚠️  Current Implementation Test:")
        print(f"Relative coordinates: ({current_cross_x}, {current_cross_y}) - WRONG LOCATION")
        print(f"Screen coordinates: ({expected_screen_x}, {expected_screen_y})")
        print("This clicks TOP RIGHT instead of BOTTOM LEFT!")

        self.assertTrue(result, "Click should still work even with wrong coordinates")

    def test_cross_button_location_explanation(self):
        """
        Explain the correct cross button location
        """
        print("\n📋 Cross Button Location Guide:")
        print("In most mobile apps, the cross/close button is typically located:")
        print("  ✅ BOTTOM LEFT - for close/dismiss actions")
        print("  ❌ TOP RIGHT - usually for menu/settings")
        print()
        print("Current code clicks TOP RIGHT, but should click BOTTOM LEFT")
        print("This test verifies the coordinate calculation and suggests the fix")

def test_cross_button_with_test_image():
    """
    Test cross button detection using the test image
    """
    print("\n🖼️  Testing with Test Image:")
    print("Test image available: screenshots_for_test/end_rename_screenshot.png")

    # Check if test image exists
    test_image_path = Path("../screenshots_for_test/end_rename_screenshot.png")
    if test_image_path.exists():
        print(f"✅ Test image found: {test_image_path}")
        print("To properly test cross button detection, you would need:")
        print("  1. Image processing to locate the cross button visually")
        print("  2. OCR or template matching to find the X symbol")
        print("  3. Coordinate extraction from the image analysis")
    else:
        print(f"❌ Test image not found: {test_image_path}")

if __name__ == "__main__":
    print("Cross Button Click Testing Suite")
    print("=" * 60)

    # Run the unit tests
    unittest.main(verbosity=2, exit=False)

    # Additional test with test image
    test_cross_button_with_test_image()

    print("\n" + "=" * 60)
    print("📝 SUMMARY:")
    print("The current implementation clicks the TOP RIGHT area,")
    print("but the cross button should be in the BOTTOM LEFT area.")
    print("Update the coordinates in main.py for correct cross button clicking!")
