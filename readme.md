# Universal Converter

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)

A simple yet powerful **desktop file converter** with a modern GUI built on **Tkinter + ttkbootstrap**.  
Supports audio, image, PDF, and more - all in one place.

---

## Requirements

The `.exe` build already includes all Python dependencies.  
You only need to install the following **external tools** on your system:

- [**FFmpeg**](https://ffmpeg.org/download.html) → required for audio/video conversions  
  Make sure `ffmpeg` is available in your system `PATH`.

- [**LibreOffice**](https://www.libreoffice.org/download/download/) → required for document conversions (e.g. DOCX → PDF)

---

## How to Use

### 1. Start the App

- Run `UniversalConverter.exe` (or `python main.py` if using source).

### 2. Pick a Converter

- Select the type of converter from the dropdown (Audio, Image, PDF, etc.).
- An **info message** below the dropdown will tell you if extra software is required  
  (e.g. *"Audio conversion requires ffmpeg installed"*).

### 3. Choose Output Format

- Select the format you want to convert to (e.g. `mp3`, `jpg`, `pdf`).

### 4. Select Input File or Folder

- Browse for a file.  
- Or enable **Batch Mode** to convert all files in a folder at once.

### 5. Upload to Temp

- Click **Upload** → the app makes a safe copy of your input(s) into a temporary folder.  
- Your originals stay untouched.

### 6. Convert

- Press **Convert**.  
- Progress and messages appear in the log box.

### 7. Find Results

- All converted files are saved into: ~/UniversalConverter/outputs

- Use **Open Output Folder** to jump directly there.

---

## Features

- ✅ **Batch mode** (convert entire folders at once)
- ✅ Safe — inputs copied to temp, originals never modified  
- ✅ Works on Windows, macOS, and Linux (However, there is only an executable for Windows)

---

## License

MIT License
© Tobias Kisling 2025
