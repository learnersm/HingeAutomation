# Hinge Automation

Automated interaction system for the Hinge dating app using scrcpy device mirroring.

## ⚠️ IMPORTANT LEGAL & ETHICAL DISCLAIMERS

### 🚫 Legal Disclaimer
**This software is provided for educational and research purposes only.** The author is not responsible for any misuse, violations of terms of service, account suspensions, bans, or any other consequences arising from the use of this software.

**POTENTIAL VIOLATION OF TERMS OF SERVICE:** Using automation tools with dating apps may violate Hinge's Terms of Service, Community Guidelines, and/or other applicable platform policies. Users are solely responsible for ensuring their usage complies with all applicable laws, regulations, and platform terms. The author explicitly disclaims any liability for violations or consequences resulting from use of this software.

### 🤖 Ethical Usage Guidelines
- **Respect Consent & Privacy:** Do not use this tool to harass, spam, or disrespect other users
- **Human-like Behavior:** Avoid excessive automation that could be detected as non-human activity
- **Rate Limiting:** Respect daily profile limits and platform-imposed restrictions
- **No Discrimination:** Ensure AI-generated content does not promote bias, harassment, or inappropriate behavior
- **Responsible AI Use:** Monitor and verify AI-generated comments before they are sent

### 🔒 Privacy & Security Notices
- **Local Processing Only:** All AI analysis and processing occurs locally on your device using Ollama
- **No Data Collection:** This software does not collect, transmit, or store personal data from profiles
- **Screenshot Security:** Profile screenshots are temporarily stored locally and automatically cleaned up
- **Device Security:** Ensure your Android device and USB connection are secure
- **Account Safety:** Using automation increases risk of account detection and suspension

### ⚠️ Safety Warnings
- **Account Risk:** Hinge may suspend or ban accounts detected using automation
- **Legal Compliance:** Ensure compliance with local laws regarding automation and data processing
- **No Warranty:** This software is provided "AS IS" without any warranties
- **Use at Your Own Risk:** The author is not liable for any damages or losses incurred

## Features

- Automated profile browsing and rating
- Screenshot capture and analysis
- Intelligent comment generation
- Error handling and cleanup

## Requirements

- Python 3.8+
- Android device with Hinge app
- USB debugging enabled
- scrcpy installed

## Installation

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install scrcpy from https://github.com/Genymobile/scrcpy
4. Connect Android device via USB

## Usage

Run the main script:
```bash
python main.py
```

## Testing

### AI Layer Testing

To test the AI layer functionality (requires Ollama to be running locally):

```bash
cd tests
python3 test_ai_layer.py
```

This will test the Ollama integration with a simple prompt and verify that the AI layer is working correctly.

### Step 7 Profile Analysis Testing

To test the complete Step 7 profile analysis and engagement functionality:

```bash
cd tests
python3 test_step7.py
```

This will test:
- Profile analysis using vision LLM
- Rating and decision logic
- Comment generation and validation
- Integration between ProfileAnalyzer and CommentGenerator

### Requirements for Testing

- Ollama installed and running locally
- Model `gemma3:4b` pulled in Ollama (or update `OLLAMA_CONFIG` in `config.py`)
- Python dependencies installed
- Screenshots in `screenshots/` directory (for full testing) or run with mock data

## Project Structure

- `main.py`: Main entry point
- `config.py`: Configuration settings
- `modules/`: Core functionality modules
- `tests/`: Test scripts and utilities
- `screenshots/`: Captured screenshots
- `logs/`: Application logs

## Modules

- `scrcpy_manager.py`: Manages scrcpy process
- `window_detector.py`: Window detection and dimensions
- `interaction_handler.py`: GUI interactions
- `screenshot_handler.py`: Screenshot capture
- `profile_analyzer.py`: Profile analysis and rating
- `comment_generator.py`: Comment generation
- `error_handler.py`: Error handling and cleanup
- `ai/`: AI layer for LLM integration
  - `llm_base.py`: LLM protocol definition
  - `ollama_client.py`: Ollama LLM implementation
  - `ai_manager.py`: LLM factory and configuration
  - `prompts.py`: Prompt templates (for future use)

## Safety Notes

- No data deletion operations
- Respect daily profile limits
- Use at your own risk

## License

MIT License
