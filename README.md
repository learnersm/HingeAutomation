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

## Testing

### AI Layer Testing

To test the AI layer functionality (requires Ollama to be running locally):

```bash
cd tests
python3 test_ai_layer.py
```

This will test the Ollama integration with a simple prompt and verify that the AI layer is working correctly.

### Requirements for AI Testing

- Ollama installed and running locally
- Model `gemma3:4b` pulled in Ollama (or update `OLLAMA_CONFIG` in `config.py`)
- Python dependencies installed

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
