"""
User Preferences Configuration
Science-based green flags and red flags for profile filtering
Based on relationship research and compatibility studies
"""

# Quick Rating Threshold
QUICK_RATING_THRESHOLD = 4  # Minimum rating to continue with full analysis

# Green Flags (Positive indicators backed by relationship research)
# These increase compatibility likelihood based on studies
GREEN_FLAGS = {
    # Age compatibility (research shows 5-7 year age gaps optimal)
    "age_range": {
        "min_age": 22,
        "max_age": 35,
        "reason": "Age range shown to have optimal relationship outcomes"
    },

    # Education correlation (studies show educational similarity predicts satisfaction)
    "education": {
        "preferred_levels": ["Bachelor's"],
        "reason": "Educational similarity correlates with relationship satisfaction"
    },

    # Physical activity (research links exercise habits to relationship quality)
    "exercise_habits": {
        "preferred": ["Regular exercise", "Active lifestyle", "Gym", "Sports"],
        "reason": "Shared activity levels predict long-term compatibility"
    },

    # Height preferences (based on population averages and stated preferences)
    "height": {
        "min_height_female": 160,  
        "max_height_female": 175, 
        "reason": "Height preferences are commonly stated and biologically relevant"
    },

    # Location proximity (research shows geographic proximity aids relationship success)
    "location": {
        "max_distance_km": 50,
        "preferred_cities": [],  # User can customize
        "reason": "Geographic proximity is a strong predictor of relationship success"
    },

    # Interests alignment (shared interests predict relationship satisfaction)
    "interests": {
        "preferred": ["Travel", "Reading", "Music", "Art", "Sports", "Cooking"],
        "reason": "Shared interests are associated with higher relationship quality"
    }
}

# Red Flags (Automatic rejection criteria backed by research)
# These are scientifically linked to relationship problems
RED_FLAGS = {
    # Smoking (research shows smoking negatively impacts relationship satisfaction)
    "smoking": {
        "keywords": ["smoker", "smoking", "cigarettes", "vape", "tobacco"],
        "severity": "high",
        "reason": "Smoking is associated with lower relationship satisfaction and health issues"
    },

    # Heavy drinking (studies link alcohol abuse to relationship problems)
    "heavy_drinking": {
        "keywords": ["heavy drinker", "party every night", "blackout", "alcoholism"],
        "severity": "high",
        "reason": "Heavy drinking correlates with relationship conflict and dissatisfaction"
    },

    # Political extremism (research shows political differences predict divorce)
    "political_extremism": {
        "keywords": ["far right", "far left", "extremist", "radical", "political zealot"],
        "severity": "medium",
        "reason": "Political extremism is linked to higher relationship conflict"
    },

    # Kids dealbreaker (stated preferences about children are highly predictive)
    "kids_dealbreaker": {
        "keywords": ["no kids ever", "anti-children", "hate kids", "never want children"],
        "severity": "high",
        "reason": "Child preferences are fundamental compatibility factors"
    },

    # Religious fundamentalism (studies show religious differences predict breakup)
    "religious_fundamentalism": {
        "keywords": ["fundamentalist", "extremely religious", "bible thumper", "jihad"],
        "severity": "medium",
        "reason": "Religious extremism correlates with relationship difficulties"
    },

    # Criminal history (obviously problematic for relationships)
    "criminal_history": {
        "keywords": ["felon", "prison", "arrested", "criminal record", "jail time"],
        "severity": "high",
        "reason": "Criminal history significantly impacts relationship viability"
    },

    # Mental health red flags (severe mental health issues)
    "severe_mental_health": {
        "keywords": ["bipolar disorder", "schizophrenia", "borderline personality", "psychosis"],
        "severity": "high",
        "reason": "Severe mental health conditions require careful consideration"
    }
}

# User Profile (for compatibility matching)
USER_PROFILE = {
    "age": 30,
    "gender": "male",
    "education": "Bachelor's",
    "height_cm": 177,
    "exercise_frequency": "regular",
    "smoking": False,
    "drinking": False,
    "has_children": False,
    "wants_children": True,
    "religion": "agnostic",
    "politics": "moderate"
}

def get_green_flags():
    """Get all green flags configuration"""
    return GREEN_FLAGS

def get_red_flags():
    """Get all red flags configuration"""
    return RED_FLAGS

def get_quick_rating_threshold():
    """Get the minimum rating threshold for continuing analysis"""
    return QUICK_RATING_THRESHOLD

def has_red_flag(text_analysis, red_flags_config=None):
    """
    Check if text analysis contains any red flags

    Args:
        text_analysis: String containing AI analysis of profile
        red_flags_config: Red flags configuration (uses global if None)

    Returns:
        tuple: (has_red_flag, red_flag_details)
    """
    if red_flags_config is None:
        red_flags_config = RED_FLAGS

    text_lower = text_analysis.lower()

    for flag_name, flag_config in red_flags_config.items():
        for keyword in flag_config["keywords"]:
            if keyword.lower() in text_lower:
                return True, {
                    "flag_name": flag_name,
                    "keyword_found": keyword,
                    "severity": flag_config["severity"],
                    "reason": flag_config["reason"]
                }

    return False, None

def calculate_compatibility_score(profile_analysis, user_profile=None):
    """
    Calculate compatibility score based on green flags

    Args:
        profile_analysis: AI analysis of profile
        user_profile: User profile data

    Returns:
        dict: Compatibility scores and recommendations
    """
    if user_profile is None:
        user_profile = USER_PROFILE

    # This would be implemented with more sophisticated matching
    # For now, return a basic structure
    return {
        "overall_score": 0.0,
        "green_flag_matches": [],
        "red_flag_warnings": [],
        "recommendation": "neutral"
    }
