# Qureo Automation Tool

A Python script to automate lesson completion on the Qureo platform using Playwright.

## Features
- **Auto Login**: Securely logs into your student account.
- **Direct Skip**: Directly marks lessons as complete via API calls.
- **Dynamic Lessons**: Automatically generates lesson IDs based on chapter and lesson numbers.
- **Video Recording**: Records a video of the session for verification.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **Run**:
   ```bash
   python main.py
   ```

## Disclaimer
This tool is for educational purposes only. Automated interaction with educational platforms should comply with their Terms of Service.

## Project Structure
- `main.py`: Entry point, handles configuration and logic.
- `engine.py`: Playwright wrapper for browser automation.
- `config.json`: Private settings (credentials and targets).
- `saved/videos/`: Directory where session recordings are stored.
