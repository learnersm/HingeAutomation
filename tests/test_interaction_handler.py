#!/usr/bin/env python3
"""
Test script for Interaction Handler module
Tests GUI interaction methods including type_text
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.interaction_handler import InteractionHandler

class TestInteractionHandler(unittest.TestCase):
    """
    Test cases for InteractionHandler class
    """

    def setUp(self):
        """Set up test fixtures"""
        self.handler = InteractionHandler()
        self.test_bounds = {
            'left': 100,
            'top': 50,
            'width': 800,
            'height': 600
        }

    def test_initialization(self):
        """Test that InteractionHandler initializes correctly"""
        self.assertIsInstance(self.handler, InteractionHandler)
        self.assertIsNone(self.handler.window_bounds)

    def test_set_window_bounds(self):
        """Test setting window bounds"""
        self.handler.set_window_bounds(self.test_bounds)
        self.assertEqual(self.handler.window_bounds, self.test_bounds)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_click_at_success(self, mock_pyautogui):
        """Test successful click operation"""
        # Setup mock
        mock_pyautogui.click.return_value = None

        # Test click
        result = self.handler.click_at(200, 300)

        # Verify
        self.assertTrue(result)
        mock_pyautogui.click.assert_called_once_with(200, 300)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_click_at_with_window_bounds(self, mock_pyautogui):
        """Test click operation with window bounds set"""
        # Setup
        self.handler.set_window_bounds(self.test_bounds)
        mock_pyautogui.click.return_value = None

        # Test click (should use raw coordinates as per current implementation)
        result = self.handler.click_at(200, 300)

        # Verify
        self.assertTrue(result)
        mock_pyautogui.click.assert_called_once_with(200, 300)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', False)
    def test_click_at_pyautogui_unavailable(self,):
        """Test click operation when pyautogui is not available"""
        result = self.handler.click_at(200, 300)
        self.assertFalse(result)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_click_at_exception(self, mock_pyautogui):
        """Test click operation with exception"""
        # Setup mock to raise exception
        mock_pyautogui.click.side_effect = Exception("Click failed")

        # Test click
        result = self.handler.click_at(200, 300)

        # Verify
        self.assertFalse(result)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_type_text_success(self, mock_pyautogui):
        """Test successful text typing"""
        # Setup mock
        mock_pyautogui.typewrite.return_value = None

        # Test typing
        test_text = "Hello, World!"
        result = self.handler.type_text(test_text)

        # Verify
        self.assertTrue(result)
        mock_pyautogui.typewrite.assert_called_once_with(test_text)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_type_text_empty_string(self, mock_pyautogui):
        """Test typing empty string"""
        # Setup mock
        mock_pyautogui.typewrite.return_value = None

        # Test typing empty string
        result = self.handler.type_text("")

        # Verify
        self.assertTrue(result)
        mock_pyautogui.typewrite.assert_called_once_with("")

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_type_text_special_characters(self, mock_pyautogui):
        """Test typing text with special characters"""
        # Setup mock
        mock_pyautogui.typewrite.return_value = None

        # Test typing special characters
        test_text = "Hello! @#$%^&*()_+{}|:<>?[]\\;',./"
        result = self.handler.type_text(test_text)

        # Verify
        self.assertTrue(result)
        mock_pyautogui.typewrite.assert_called_once_with(test_text)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_type_text_unicode_characters(self, mock_pyautogui):
        """Test typing text with unicode characters"""
        # Setup mock
        mock_pyautogui.typewrite.return_value = None

        # Test typing unicode characters
        test_text = "Hello 🌟 你好 Привет"
        result = self.handler.type_text(test_text)

        # Verify
        self.assertTrue(result)
        mock_pyautogui.typewrite.assert_called_once_with(test_text)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_type_text_long_string(self, mock_pyautogui):
        """Test typing very long text"""
        # Setup mock
        mock_pyautogui.typewrite.return_value = None

        # Test typing long string
        test_text = "A" * 1000  # 1000 character string
        result = self.handler.type_text(test_text)

        # Verify
        self.assertTrue(result)
        mock_pyautogui.typewrite.assert_called_once_with(test_text)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', False)
    def test_type_text_pyautogui_unavailable(self):
        """Test type_text when pyautogui is not available"""
        result = self.handler.type_text("test text")
        self.assertFalse(result)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_type_text_exception(self, mock_pyautogui):
        """Test type_text with exception"""
        # Setup mock to raise exception
        mock_pyautogui.typewrite.side_effect = Exception("Typing failed")

        # Test typing
        result = self.handler.type_text("test text")

        # Verify
        self.assertFalse(result)

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_swipe_success(self, mock_pyautogui):
        """Test successful swipe operation"""
        # Setup mock
        mock_pyautogui.moveTo.return_value = None
        mock_pyautogui.dragTo.return_value = None

        # Test swipe
        result = self.handler.swipe(100, 200, 300, 400)

        # Verify
        self.assertTrue(result)
        mock_pyautogui.moveTo.assert_called_once_with(100, 200)
        mock_pyautogui.dragTo.assert_called_once_with(300, 400, duration=0.5, button='left')

    @patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True)
    @patch('modules.interaction_handler.pyautogui')
    def test_swipe_with_window_bounds(self, mock_pyautogui):
        """Test swipe operation with window bounds set"""
        # Setup
        self.handler.set_window_bounds(self.test_bounds)
        mock_pyautogui.moveTo.return_value = None
        mock_pyautogui.dragTo.return_value = None

        # Test swipe
        result = self.handler.swipe(50, 100, 150, 200)

        # Verify coordinates are translated
        expected_start_x = self.test_bounds['left'] + 50
        expected_start_y = self.test_bounds['top'] + 100
        expected_end_x = self.test_bounds['left'] + 150
        expected_end_y = self.test_bounds['top'] + 200

        self.assertTrue(result)
        mock_pyautogui.moveTo.assert_called_once_with(expected_start_x, expected_start_y)
        mock_pyautogui.dragTo.assert_called_once_with(expected_end_x, expected_end_y, duration=0.5, button='left')

def run_type_text_specific_tests():
    """
    Run tests specifically focused on type_text method
    """
    print("🧪 Running type_text Method Specific Tests")
    print("=" * 50)

    handler = InteractionHandler()

    # Test cases for type_text
    test_cases = [
        ("Empty string", ""),
        ("Simple text", "Hello World"),
        ("Special characters", "!@#$%^&*()"),
        ("Numbers", "1234567890"),
        ("Mixed content", "Hello123!@#"),
        ("Long text", "A" * 100),
        ("Unicode", "Hello 🌟"),
        ("Newlines", "Line 1\nLine 2"),
        ("Tabs", "Col1\tCol2\tCol3"),
    ]

    passed = 0
    total = len(test_cases)

    for test_name, test_text in test_cases:
        print(f"\nTesting: {test_name}")
        print(f"Text: '{test_text[:50]}{'...' if len(test_text) > 50 else ''}'")

        try:
            # Mock the actual typing to avoid GUI interactions during testing
            with patch('modules.interaction_handler.pyautogui') as mock_pyautogui:
                with patch('modules.interaction_handler.PYAUTOGUI_AVAILABLE', True):
                    mock_pyautogui.typewrite.return_value = None

                    result = handler.type_text(test_text)

                    if result:
                        print("✅ PASSED")
                        passed += 1
                    else:
                        print("❌ FAILED - Returned False")

        except Exception as e:
            print(f"❌ FAILED - Exception: {e}")

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All type_text tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")

    return passed == total

if __name__ == "__main__":
    print("Interaction Handler Test Suite")
    print("=" * 40)

    # Run specific type_text tests
    type_text_success = run_type_text_specific_tests()

    print("\n" + "=" * 40)
    print("Running Full Test Suite...")
    print("=" * 40)

    # Run full unittest suite
    unittest.main(verbosity=2, exit=False)

    print("\n" + "=" * 40)
    print("📝 SUMMARY:")
    print("✅ type_text method tests completed")
    print("✅ Full test suite executed")
    print("✅ Mock-based testing implemented")
    print()
    print("Usage Example:")
    print("handler = InteractionHandler()")
    print("handler.type_text('Hello, World!')")
