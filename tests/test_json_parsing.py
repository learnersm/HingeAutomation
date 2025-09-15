#!/usr/bin/env python3
"""
Test script to verify JSON parsing functionality
"""

import sys
import os
import json

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.profile_analyzer import ProfileAnalyzer

def test_json_parsing():
    """
    Test JSON parsing with mock responses
    """
    print("Testing JSON Parsing Functionality")
    print("=" * 50)

    analyzer = ProfileAnalyzer()

    # Test valid JSON response
    valid_json = '''{
        "rating": 8,
        "reason": "Attractive appearance and great personality indicators",
        "decision": "ENGAGE",
        "comment": "Love your hiking photos! What's your favorite trail?"
    }'''

    print("Testing valid JSON response...")
    result = analyzer._parse_analysis_response(valid_json)
    print(f"  Rating: {result['rating']}")
    print(f"  Decision: {result['decision']}")
    print(f"  Comment: {result['comment']}")
    print(f"  Reason: {result['reason']}")

    # Test invalid JSON response (should fallback gracefully)
    invalid_json = "RATING: 7/10\nREASON: Good profile\nDECISION: ENGAGE\nCOMMENT: Nice!"

    print("\nTesting invalid JSON response (fallback)...")
    result = analyzer._parse_analysis_response(invalid_json)
    print(f"  Rating: {result['rating']} (should be 5)")
    print(f"  Decision: {result['decision']}")
    print(f"  Comment: {result['comment']}")
    print(f"  Reason: {result['reason']}")

    # Test quick analysis JSON
    quick_json = '''{
        "rating": 6,
        "reason": "Decent profile, worth considering"
    }'''

    print("\nTesting quick analysis JSON...")
    result = analyzer._parse_quick_analysis_response(quick_json)
    print(f"  Rating: {result['rating']}")
    print(f"  Reason: {result['reason']}")

    print("\n✅ JSON parsing tests completed!")

if __name__ == "__main__":
    test_json_parsing()
