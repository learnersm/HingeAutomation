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
RATING_THRESHOLD = 6
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
# Note: When multiple ADB devices are connected, use one of these options:
# --select-usb : Select USB device (recommended)
# --select-tcpip : Select TCP/IP device
# -s <serial> : Select specific device by serial number
SCRCPY_OPTIONS = [
    "--window-title=HingeAutomation",
    "--max-size=1080",
    "--video-bit-rate=8M",
    "--select-usb"  # Select USB device when multiple devices are connected
]

# AI settings
AI_PROVIDER = "ollama"  # Default AI provider

OLLAMA_CONFIG = {
    "model": "gemma3:4b",
    "host": None,  # Use default Ollama host if None
    "options": {
        "temperature": 0.7,
        "num_predict": 256
    },
    "timeout_s": 30,
    "max_retries": 2
}

STRING_TO_INDICATE_AI_GENERATED_MESSAGE = "-AI gen"

# UI Text Detection Strings
# Used for OCR-based detection of specific UI screens
UI_TEXT_STRINGS = {
    "send_rose_instead": "send a rose instead",
    "send_like_anyway": "send like anyway",
    "daily_limit_reached": "daily limit reached",
    "profile_not_available": "profile not available",
    # AI enabled reply options screen text strings
    "ai_enabled_reply_give_feedback": "Give feedback",
    "ai_enabled_reply_hinge_learning": "Hinge is still learning"

}
