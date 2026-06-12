#  FileZip — File Compressor & Extractor

A lightweight desktop app to compress files and folders into ZIP archives, and extract them back. Built with Python and Tkinter.

---

##  Features

-Compress individual files or entire folders into ZIP
- Extract any ZIP file with a live progress bar
- Preview ZIP contents before extracting
- Shows original size, compressed size, and space saved
- Auto opens destination folder after extraction
- Clean dark-themed UI

---
## 📸 Screenshots

### Compress
![Compress Tab](screenshots/compress.png)

### Extract
![Extract Tab](screenshots/extract.png)
---

##  Getting Started

### Run from source

1. **Clone the repo**
   ```bash
   git clone https://github.com/iswarya-0901/file-compressor.git
   cd file-compressor
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
file-compressor/
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


