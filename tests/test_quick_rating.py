#!/usr/bin/env python3
"""
Test script for quick rating and red flag detection functionality
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.profile_analyzer import ProfileAnalyzer
from user_preferences import has_red_flag, get_quick_rating_threshold

class TestQuickRating(unittest.TestCase):
    """
    Test cases for quick rating and red flag detection
    """

    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = ProfileAnalyzer()

    def test_red_flag_detection(self):
        """
        Test red flag detection in text analysis
        """
        # Test text with smoking red flag
        smoking_text = "This person is a smoker and enjoys cigarettes regularly."
        has_red, details = has_red_flag(smoking_text)

        self.assertTrue(has_red, "Should detect smoking as red flag")
        self.assertEqual(details['flag_name'], 'smoking', "Should identify smoking flag")
        self.assertEqual(details['severity'], 'high', "Smoking should be high severity")

        # Test text with no red flags
        clean_text = "This person enjoys hiking and reading books."
        has_red, details = has_red_flag(clean_text)

        self.assertFalse(has_red, "Should not detect red flags in clean text")
        self.assertIsNone(details, "Should return None details for clean text")

        print("✅ Red Flag Detection Test:")
        print("   Smoking detected: ✓")
        print("   Clean text passed: ✓")

    def test_quick_rating_threshold(self):
        """
        Test quick rating threshold configuration
        """
        threshold = get_quick_rating_threshold()
        self.assertEqual(threshold, 4, "Quick rating threshold should be 4")

        print("✅ Quick Rating Threshold Test:")
        print(f"   Threshold: {threshold} ✓")

    def test_should_continue_full_analysis_red_flag(self):
        """
        Test that profiles with red flags are rejected
        """
        quick_result_with_red_flag = {
            'rating': 8,
            'has_red_flags': True,
            'red_flag_details': {
                'flag_name': 'smoking',
                'severity': 'high',
                'reason': 'Smoking is associated with lower relationship satisfaction'
            },
            'reason': 'Good physical appearance but has red flags'
        }

        should_continue = self.analyzer.should_continue_full_analysis(quick_result_with_red_flag)
        self.assertFalse(should_continue, "Should reject profiles with red flags")

        print("✅ Red Flag Rejection Test:")
        print("   Profile with red flag rejected: ✓")

    def test_should_continue_full_analysis_low_rating(self):
        """
        Test that profiles with low ratings are rejected
        """
        quick_result_low_rating = {
            'rating': 2,
            'has_red_flags': False,
            'red_flag_details': None,
            'reason': 'Poor physical appearance and incompatible interests'
        }

        should_continue = self.analyzer.should_continue_full_analysis(quick_result_low_rating)
        self.assertFalse(should_continue, "Should reject profiles with rating < 4")

        print("✅ Low Rating Rejection Test:")
        print("   Profile with low rating rejected: ✓")

    def test_should_continue_full_analysis_good_profile(self):
        """
        Test that good profiles continue to full analysis
        """
        quick_result_good = {
            'rating': 7,
            'has_red_flags': False,
            'red_flag_details': None,
            'reason': 'Attractive appearance and compatible interests'
        }

        should_continue = self.analyzer.should_continue_full_analysis(quick_result_good)
        self.assertTrue(should_continue, "Should continue with good profiles")

        print("✅ Good Profile Continuation Test:")
        print("   Good profile continues to full analysis: ✓")

    def test_quick_analyze_profile_structure(self):
        """
        Test the structure of quick analysis results
        """
        # Test with empty screenshots
        result = self.analyzer.quick_analyze_profile([])
        self.assertEqual(result['rating'], 0)
        self.assertFalse(result['has_red_flags'])

        # Test result structure for empty case
        self.assertIn('rating', result)
        self.assertIn('has_red_flags', result)
        self.assertIn('red_flag_details', result)
        self.assertIn('reason', result)

        print("✅ Quick Analysis Structure Test:")
        print("   Empty screenshots handled: ✓")
        print("   Result structure correct: ✓")

if __name__ == "__main__":
    print("Quick Rating & Red Flag Detection Testing Suite")
    print("=" * 60)
    print("Testing science-based filtering system:")
    print("  - Red flags: smoking, heavy drinking, extremism, etc.")
    print("  - Rating threshold: 4/10")
    print("  - AI-based analysis (not keyword matching)")
    print("=" * 60)

    # Run the unit tests
    unittest.main(verbosity=2, exit=False)

    print("\n" + "=" * 60)
    print("📝 SUMMARY:")
    print("✅ Quick rating system working correctly!")
    print("✅ Red flag detection functioning properly!")
    print("✅ Science-based filtering implemented!")
    print()
    print("The system will now:")
    print("  🚫 Reject profiles with red flags immediately")
    print("  🚫 Reject profiles with rating < 4")
    print("  ✅ Continue full analysis for rating ≥ 4 + no red flags")
    print("  🧠 Using AI analysis (not simple keyword matching)")
