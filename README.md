# AI-Enabled Scientific Calculator (Python + Tkinter)

This is a GitHub-ready project for a **Scientific Calculator** built with Python and Tkinter.
It implements:
- Basic arithmetic operations (+, -, *, /, %, .)
- Scientific functions (sin, cos, tan, log10, ln, sqrt, factorial, exp)
- Memory (M+, M-, MR, MC)
- Calculation history with export to text
- Light and dark themes
- Optional voice input/output (uses `SpeechRecognition` + `pyttsx3`)

## Files
- `main.py` — The main application file (Tkinter GUI)
- `requirements.txt` — Python packages useful for optional voice features
- `README.md` — This file

## How to run
1. Make sure you have Python 3.8+ installed.
2. (Optional) create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
3. Install dependencies (optional for voice features):
   ```bash
   pip install -r requirements.txt
   ```
   If you don't need voice features, you can run the app without installing those packages.
4. Run:
   ```bash
   python main.py
   ```

## Voice & Microphone notes
- Voice input uses the microphone. On some systems you need to install `pyaudio` or `pipwin` (Windows) to get a working microphone driver.
- If voice packages are not available the app will still run; the "Voice" button will show a message.

## Exporting History
- Use the **History** button to export all recorded calculations to a `.txt` file.

## License
Feel free to use this in your project. Cite or adapt as needed.