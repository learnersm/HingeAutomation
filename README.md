# Hinge Automation

Automated interaction system for the Hinge dating app using scrcpy device mirroring.

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

## Project Structure

- `main.py`: Main entry point
- `config.py`: Configuration settings
- `modules/`: Core functionality modules
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

## Safety Notes

- No data deletion operations
- Respect daily profile limits
- Use at your own risk

## License

MIT License
