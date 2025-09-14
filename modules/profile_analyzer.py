"""
Profile Analyzer Module
Handles image/text analysis and rating logic for Step 7
"""

import logging
import re
from typing import List, Dict, Any
from config import RATING_THRESHOLD, MAX_RATING
from ai.ai_manager import get_llm
from ai.prompts import get_step7_analysis_prompt

class ProfileAnalyzer:
    def __init__(self, llm=None):
        self.current_profile = None
        self.llm = llm or get_llm()

    def analyze_profile(self, screenshots: List[str]) -> Dict[str, Any]:
        """
        Analyze profile from screenshots using vision LLM

        Args:
            screenshots: List of screenshot file paths

        Returns:
            Dict containing:
            - rating: int (1-10)
            - decision: str ('ENGAGE' or 'NEXT_PROFILE')
            - comment: str (witty comment or 'N/A')
            - reason: str (explanation of rating)
        """
        if not screenshots:
            return {
                'rating': 0,
                'decision': 'NEXT_PROFILE',
                'comment': 'N/A',
                'reason': 'No screenshots provided'
            }

        try:
            # Get the Step 7 analysis prompt
            prompt = get_step7_analysis_prompt()

            # Generate analysis using vision capabilities
            logging.info(f"Sending {len(screenshots)} screenshots to LLM for analysis")
            response = self.llm.generate(
                prompt=prompt,
                images=screenshots,
                options={"temperature": 0.7, "num_predict": 300}
            )

            # Log the raw LLM response
            logging.info(f"LLM Raw Response: {response}")

            # Parse the structured response
            return self._parse_analysis_response(response)

        except Exception as e:
            logging.error(f"Profile analysis failed: {e}")
            return {
                'rating': 0,
                'decision': 'NEXT_PROFILE',
                'comment': 'N/A',
                'reason': f'Analysis failed: {str(e)}'
            }

    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM response into structured data

        Args:
            response: Raw LLM response

        Returns:
            Parsed analysis result
        """
        result = {
            'rating': 0,
            'decision': 'NEXT_PROFILE',
            'comment': 'N/A',
            'reason': 'Failed to parse response'
        }

        try:
            lines = response.strip().split('\n')

            for line in lines:
                line = line.strip()
                if line.startswith('RATING:'):
                    # Extract rating (e.g., "RATING: 8/10" -> 8)
                    rating_match = re.search(r'RATING:\s*(\d+)/10', line)
                    if rating_match:
                        result['rating'] = int(rating_match.group(1))

                elif line.startswith('REASON:'):
                    result['reason'] = line.replace('REASON:', '').strip()

                elif line.startswith('DECISION:'):
                    decision = line.replace('DECISION:', '').strip().upper()
                    if decision in ['ENGAGE', 'NEXT_PROFILE']:
                        result['decision'] = decision

                elif line.startswith('COMMENT:'):
                    comment = line.replace('COMMENT:', '').strip()
                    if comment and comment != 'N/A':
                        # Ensure comment is under 150 characters
                        if len(comment) > 150:
                            comment = comment[:147] + '...'
                        result['comment'] = comment

            # Validate rating range
            if not (1 <= result['rating'] <= 10):
                result['rating'] = 5  # Default to middle rating
                result['reason'] = 'Invalid rating, defaulting to 5'

        except Exception as e:
            logging.error(f"Failed to parse analysis response: {e}")
            result['reason'] = f'Parse error: {str(e)}'

        return result

    def should_engage_profile(self, analysis_result: Dict[str, Any]) -> bool:
        """
        Determine if we should engage with the profile based on analysis

        Args:
            analysis_result: Result from analyze_profile

        Returns:
            bool: True if should engage, False otherwise
        """
        return (analysis_result.get('decision') == 'ENGAGE' and
                analysis_result.get('rating', 0) >= RATING_THRESHOLD and
                analysis_result.get('comment') not in ['N/A', ''])
