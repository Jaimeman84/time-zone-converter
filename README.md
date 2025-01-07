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

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/jaimeman84/time-zone-converter.git
cd timezone-converter
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install streamlit pytz pytest
```

4. Run the app:
```bash
streamlit run app.py
```

5. Open `http://localhost:8501` in your browser

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

## Troubleshooting

If you encounter any issues:
1. Make sure your virtual environment is activated
2. Verify all dependencies are installed correctly
3. Check if you're using Python 3.8 or higher

## License

MIT License

---
Made with Python and Streamlit