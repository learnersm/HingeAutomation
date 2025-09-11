"""
Configuration settings for Hinge Automation
"""

# Window settings
WINDOW_TITLE = "HingeAutomation"
DEFAULT_WINDOW_WIDTH = 1080
DEFAULT_WINDOW_HEIGHT = 1920

# Timeouts (in seconds)
TIMEOUTS = {
    "scrcpy_start": 5,
    "window_detection": 3,
    "profile_load": 10,
    "screenshot_capture": 2,
    "interaction_delay": 1,
    "scroll_wait": 2
}

# Rating settings
RATING_THRESHOLD = 7
MAX_RATING = 10

# Screenshot settings
SCREENSHOT_DIR = "screenshots"
SCREENSHOT_FORMAT = "png"

# Logging settings
LOG_DIR = "logs"
LOG_LEVEL = "INFO"

# Comment settings
MAX_COMMENT_LENGTH = 150

# Error handling
MAX_RETRY_ATTEMPTS = 3
DAILY_LIMIT_MESSAGE = "Limit of daily profiles reached"

# Scrcpy settings
SCRCPY_OPTIONS = [
    "--no-control",
    "--window-title=HingeAutomation",
    "--max-size=1080",
    "--video-bit-rate=8M"
]
