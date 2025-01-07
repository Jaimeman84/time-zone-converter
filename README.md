# Time Zone Converter 🌍

A simple time zone converter app that shows the current time across 5 major time zones based on EST input. Built with Python and Streamlit.

## Features

- Convert EST time to 5 major time zones:
  - New York (EST)
  - Los Angeles (PST)
  - London (GMT)
  - Paris (CET)
  - Tokyo (JST)
- Color-coded time cards for easy time difference visualization
- Simple and clean user interface

## Requirements

- Python 3.8+
- pip

## Quick Start

1. Install dependencies:
```bash
pip install streamlit pytz pytest
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open `http://localhost:8501` in your browser

## Project Structure

```
timezone-converter/
├── app.py              # Main application
├── timezone_utils.py   # Utility functions
└── test_app.py        # Tests
```

## Running Tests

```bash
pytest test_app.py -v
```

## Color Guide

- 🟢 Green: Similar time zone (±3 hours)
- 🟡 Orange: Moderate difference (±4-6 hours)
- 🔴 Red: Large time difference (>6 hours)

## License

MIT License

---
Made with Python and Streamlit