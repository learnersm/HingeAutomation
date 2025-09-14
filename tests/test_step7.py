#!/usr/bin/env python3
"""
Test script for Step 7: Profile Analysis & Engagement
Tests the complete profile analysis workflow
"""

import sys
import os
from pathlib import Path

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.profile_analyzer import ProfileAnalyzer
from modules.comment_generator import CommentGenerator

def test_step7_with_existing_screenshots():
    """
    Test Step 7 functionality using existing screenshots
    """
    print("Testing Step 7: Profile Analysis & Engagement...")

    # Check if screenshots directory exists and has files
    screenshots_dir = Path("../screenshots")
    if not screenshots_dir.exists():
        print("❌ Screenshots directory not found")
        return False

    screenshot_files = list(screenshots_dir.glob("*.png"))
    if not screenshot_files:
        print("❌ No screenshot files found in screenshots directory")
        return False

    print(f"Found {len(screenshot_files)} screenshot files:")
    for f in screenshot_files:
        print(f"  - {f.name}")

    try:
        # Initialize components
        analyzer = ProfileAnalyzer()
        generator = CommentGenerator()

        # Convert Path objects to strings for the analyzer
        screenshot_paths = [str(f) for f in screenshot_files]

        # Test profile analysis
        print("\n🔍 Analyzing profile...")

        # Enable logging to see LLM response
        import logging
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

        analysis_result = analyzer.analyze_profile(screenshot_paths)

        print("\n📊 Analysis Results:")
        print(f"  Rating: {analysis_result['rating']}/10")
        print(f"  Decision: {analysis_result['decision']}")
        print(f"  Reason: {analysis_result['reason']}")
        print(f"  Comment: {analysis_result['comment']}")

        # Test engagement decision
        should_engage = analyzer.should_engage_profile(analysis_result)
        print(f"  Should Engage: {should_engage}")

        # Test comment validation if we have a comment
        if analysis_result['comment'] and analysis_result['comment'] != 'N/A':
            is_valid = generator.validate_comment(analysis_result['comment'])
            print(f"  Comment Valid: {is_valid} (Length: {len(analysis_result['comment'])})")

        print("\n✅ Step 7 test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Step 7 test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_step7_with_mock_data():
    """
    Test Step 7 with mock data when no screenshots are available
    """
    print("Testing Step 7 with mock data (no screenshots available)...")

    try:
        analyzer = ProfileAnalyzer()

        # Test with empty screenshot list
        result = analyzer.analyze_profile([])
        print("Empty screenshots test:")
        print(f"  Rating: {result['rating']}")
        print(f"  Decision: {result['decision']}")
        print(f"  Reason: {result['reason']}")

        # Test decision logic
        should_engage = analyzer.should_engage_profile(result)
        print(f"  Should Engage: {should_engage}")

        print("✅ Mock data test completed!")
        return True

    except Exception as e:
        print(f"❌ Mock data test failed: {e}")
        return False

if __name__ == "__main__":
    print("Step 7 Testing Suite")
    print("=" * 50)

    # Test with existing screenshots if available
    success1 = test_step7_with_existing_screenshots()

    # Always test with mock data
    success2 = test_step7_with_mock_data()

    if success1 or success2:
        print("\n🎉 Step 7 testing completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 All Step 7 tests failed!")
        sys.exit(1)
