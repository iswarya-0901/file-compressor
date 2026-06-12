#  FileZip — File Compressor

A lightweight desktop app to compress files and folders into ZIP archives. Built with Python and Tkinter.

---

##  Features

- Add individual files or entire folders
- Real-time compression progress bar
- Shows original size, compressed size, and space saved
- Clean dark-themed UI
- Runs on Windows, macOS, and Linux

---

##  Getting Started

### Run from source

1. **Clone the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/FileZip.git
   cd FileZip
   ```

2. **Install dependencies** *(only needed to build the .exe)*
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

---

##  Build the `.exe` (Windows)

```bash
pyinstaller --onefile --windowed --name "FileZip" app.py
```

The output will be at `dist/FileZip.exe` — a standalone executable, no Python required.

To add a custom icon:
```bash
pyinstaller --onefile --windowed --name "FileZip" --icon="assets/icon.ico" app.py
```

---

##  Project Structure

```
FileZip/
├── app.py              # Main application
├── requirements.txt    # Build dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── assets/             # Icons and images (optional)
```

---

##  Dependencies

- **Python 3.8+** — standard library only (`tkinter`, `zipfile`, `threading`)
- **PyInstaller** — only needed to build the `.exe`


