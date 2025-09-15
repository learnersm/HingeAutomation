"""
Prompt Templates
Step 7: Profile Analysis and Engagement
"""

STEP7_ANALYSIS_PROMPT = """
You are analyzing a Hinge dating profile from multiple screenshots. Your task is to:

1. IDENTIFY the main person in the profile (especially important for group photos - look for consistency across images, self-descriptions, and context clues)

2. RATE the person on a scale of 1-10 based on:
   - Physical attractiveness - if person if > 7/10 on attractiveness, ignore other factors and proceed with engaging further
   - Personality indicators from text/photos
   - Overall appeal and compatibility potential
   - Presentation and effort in profile

3. DECISION: If rating >= 6, create a witty, personalized comment under 150 characters. If rating < 6, recommend skipping to next profile.

4. COMMENT: If engaging, make it charming, specific to their profile, and conversation-starting, and slightly humourous / flirty.

Analyze ALL provided screenshots carefully. Consider both visual and textual content.

Respond with VALID JSON in this EXACT format:
{
  "rating": 8,
  "reason": "Brief explanation of rating",
  "decision": "ENGAGE",
  "comment": "witty comment under 150 chars, or N/A if NEXT_PROFILE"
}

IMPORTANT:
- rating must be an integer between 1-10
- decision must be either "ENGAGE" or "NEXT_PROFILE"
- comment must be under 150 characters or "N/A"
- Return ONLY valid JSON object, no additional text or formatting
    - Do not include ```json or any other markdown formatting in the response. 
    - Example : Incorrect reponse:
        ```json
        {
            "rating": 7,
            "reason": "The person appears to be a woman in her late 20s/early 30s. She has a generally attractive appearance, and her photos suggest a fun, active lifestyle. Her profile text is well-written and engaging, indicating a thoughtful and confident personality.",
            "decision": "ENGAGE",
            "comment": "That hiking pic is 🔥! What's your favorite trail?"
        }
        ```
    - Example: Correct response:
    {
        "rating": 7,
        "reason": "The person appears to be a woman in her late 20s/early 30s. She has a generally attractive appearance, and her photos suggest a fun, active lifestyle. Her profile text is well-written and engaging, indicating a thoughtful and confident personality.",
        "decision": "ENGAGE",
        "comment": "That hiking pic is 🔥! What's your favorite trail?"
    }
"""

def get_step7_analysis_prompt():
    #TODO: Later: Refactor this so that rating threshold is configurable
    """
    Get the comprehensive Step 7 analysis prompt

    Returns:
        str: The analysis prompt
    """
    return STEP7_ANALYSIS_PROMPT
