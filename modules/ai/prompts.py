"""
Prompt Templates
Step 7: Profile Analysis and Engagement
"""

STEP7_ANALYSIS_PROMPT = """
You are analyzing a Hinge dating profile from multiple screenshots. Your task is to:

1. IDENTIFY the main person in the profile (especially important for group photos - look for consistency across images, self-descriptions, and context clues)

2. RATE the person on a scale of 1-10 based on:
   - Physical attractiveness
   - Personality indicators from text/photos
   - Overall appeal and compatibility potential
   - Presentation and effort in profile

3. DECISION: If rating >= 7, create a witty, personalized comment under 150 characters. If rating < 7, recommend skipping to next profile.

4. COMMENT: If engaging, make it charming, specific to their profile, and conversation-starting.

Analyze ALL provided screenshots carefully. Consider both visual and textual content.

Respond in this EXACT format:

RATING: X/10
REASON: Brief explanation of rating
DECISION: ENGAGE/NEXT_PROFILE
COMMENT: [witty comment under 150 chars, or "N/A" if NEXT_PROFILE]
"""

def get_step7_analysis_prompt():
    """
    Get the comprehensive Step 7 analysis prompt

    Returns:
        str: The analysis prompt
    """
    return STEP7_ANALYSIS_PROMPT
