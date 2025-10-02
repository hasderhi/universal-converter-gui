"""
Universal Converter
"""

import os
import sys
import shutil
import tempfile
import uuid
import threading
import webbrowser
import subprocess
from pathlib import Path

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, StringVar, Text, END, DISABLED, NORMAL, BooleanVar, Scrollbar, RIGHT, Y

# make sure pyinstaller includes everything
from converters.base import Converter
from converters.audio import AudioConverter
from converters.excel_converter import ExcelConverter
from converters.image import ImageConverter
from converters.office_pdf import OfficeToPDFConverter

try:
    from converters import load_converters
except Exception as e:
    messagebox.showerror("Import Error", f"Failed importing converters: {e}")
    raise

converters = load_converters()
if not converters:
    messagebox.showerror("No converters", "No converters found. Check your project setup.")
    sys.exit(1)

TEMP_DIR = Path(tempfile.gettempdir()) / "universal_converter_gui"
OUTPUT_DIR = Path.home() / "UniversalConverter" / "outputs"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def converter_by_name(name):
    return next((c for c in converters if getattr(c, "name", None) == name), None)

def copy_to_temp(filepath: str) -> Path:
    filename = os.path.basename(filepath)
    dest = TEMP_DIR / f"{uuid.uuid4()}_{filename}"
    shutil.copy2(filepath, dest)
    return dest

def run_conversion(inputs, converter, out_format, log_widget, root, finish_callback):
    try:
        results = []
        for f in inputs:
            append_log(log_widget, f"Converting {Path(f).name} -> {out_format}")
            out_path = converter.convert(f, out_format, {"output_dir": str(OUTPUT_DIR)})

            # Ensure output file ends up in OUTPUT_DIR
            out_path = Path(out_path)
            if not str(out_path).startswith(str(OUTPUT_DIR)):
                out_file = OUTPUT_DIR / out_path.name
                try:
                    shutil.move(str(out_path), str(out_file))
                    out_path = out_file
                except Exception:
                    shutil.copy2(str(out_path), str(out_file))
                    out_path = out_file

            results.append(str(out_path))

        root.after(0, lambda: finish_callback(results, None))
    except Exception as e:
        err = str(e)
        root.after(0, lambda err=err: finish_callback(None, err))

def append_log(widget, text):
    widget.config(state=NORMAL)
    widget.insert(END, text + "\n")
    widget.see(END)
    widget.config(state=DISABLED)

# GUI
root = tb.Window(themename="superhero")
root.title("Universal Converter")
root.geometry("1100x800")

icon_path = Path(__file__).parent / "universalconverter.ico"
root.iconbitmap(str(icon_path.resolve()))

# Vars
selected_file = StringVar()
selected_converter = StringVar(value=converters[0].name)
selected_format = StringVar()
batch_mode = BooleanVar(value=False)
uploaded_temp_paths = []
last_output_paths = []

frame = tb.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=True)

tb.Label(frame, text="Universal Converter", font=("Segoe UI", 20, "bold"), bootstyle="primary").pack(pady=10)

conv_card = tb.Labelframe(frame, text="Converter Selection", padding=15, bootstyle="info")
conv_card.pack(fill=X, pady=10)

conv_frame = tb.Frame(conv_card)
conv_frame.pack(fill=X, pady=5)
tb.Label(conv_frame, text="Converter:", width=15).pack(side=LEFT)
conv_box = tb.Combobox(conv_frame, textvariable=selected_converter, values=[c.name for c in converters], state="readonly")
conv_box.pack(fill=X, expand=True)

conv_info = tb.Label(conv_card, text="", bootstyle=WARNING)
conv_info.pack(fill=X, pady=5)


fmt_frame = tb.Frame(conv_card)
fmt_frame.pack(fill=X, pady=5)
tb.Label(fmt_frame, text="Output format:", width=15).pack(side=LEFT)
fmt_box = tb.Combobox(fmt_frame, textvariable=selected_format, state="readonly")
fmt_box.pack(fill=X, expand=True)

batch_chk = tb.Checkbutton(conv_card, text="Batch mode (folder)", variable=batch_mode, bootstyle="info-round-toggle")
batch_chk.pack(pady=5)

input_card = tb.Labelframe(frame, text="Input Selection", padding=15, bootstyle="info")
input_card.pack(fill=X, pady=10)

file_frame = tb.Frame(input_card)
file_frame.pack(fill=X, pady=5)
tb.Label(file_frame, text="Input path:", width=15).pack(side=LEFT)
file_entry = tb.Entry(file_frame, textvariable=selected_file, state="readonly")
file_entry.pack(fill=X, expand=True, side=LEFT, padx=5)
tb.Button(file_frame, text="Browse", bootstyle=PRIMARY, command=lambda: choose_input()).pack(side=LEFT)

upload_btn = tb.Button(input_card, text="Upload (Temp)", bootstyle=INFO, command=lambda: upload_files())
upload_btn.pack(pady=5, anchor="e")

btn_frame = tb.Frame(frame)
btn_frame.pack(pady=10)
convert_btn = tb.Button(btn_frame, text="Convert", bootstyle=SUCCESS, command=lambda: start_conversion())
convert_btn.pack(side=LEFT, padx=10)
open_btn = tb.Button(btn_frame, text="Open Output Folder", bootstyle=SECONDARY, state=DISABLED, command=lambda: open_output())
open_btn.pack(side=LEFT, padx=10)

log_card = tb.Labelframe(frame, text="Conversion Log", padding=10, bootstyle="dark")
log_card.pack(fill=BOTH, expand=True, pady=10)

log_box = Text(log_card, height=12, wrap="word", state=DISABLED, bg="#1e1e1e", fg="white", insertbackground="white")
log_box.pack(fill=BOTH, expand=True, side=LEFT, padx=(0,2))
scrollbar = Scrollbar(log_card, command=log_box.yview)
scrollbar.pack(side=RIGHT, fill=Y)
log_box.config(yscrollcommand=scrollbar.set)

def update_formats(*_):
    conv = converter_by_name(selected_converter.get())
    if conv:
        fmt_box["values"] = conv.output_formats
        if conv.output_formats:
            selected_format.set(conv.output_formats[0])
        conv_info.config(text=getattr(conv, "info", ""))

conv_box.bind("<<ComboboxSelected>>", update_formats)
update_formats()

def choose_input():
    if batch_mode.get():
        path = filedialog.askdirectory()
    else:
        path = filedialog.askopenfilename()
    if path:
        selected_file.set(path)

def upload_files():
    path = selected_file.get()
    if not path:
        messagebox.showwarning("No input", "Please select a file/folder first")
        return
    uploaded_temp_paths.clear()
    try:
        if batch_mode.get():
            for fname in os.listdir(path):
                fpath = os.path.join(path, fname)
                if os.path.isfile(fpath):
                    uploaded_temp_paths.append(copy_to_temp(fpath))
            append_log(log_box, f"Uploaded {len(uploaded_temp_paths)} files to temp")
        else:
            uploaded_temp_paths.append(copy_to_temp(path))
            append_log(log_box, f"Uploaded to temp: {uploaded_temp_paths[0]}")
    except Exception as e:
        messagebox.showerror("Upload failed", str(e))

def start_conversion():
    if not uploaded_temp_paths:
        messagebox.showwarning("No file", "Upload input first")
        return
    out_fmt = selected_format.get()
    conv = converter_by_name(selected_converter.get())
    if not conv or not out_fmt:
        messagebox.showwarning("Missing info", "Please select converter and format")
        return

    convert_btn.config(state=DISABLED)
    open_btn.config(state=DISABLED)

    t = threading.Thread(target=run_conversion,
                         args=(uploaded_temp_paths, conv, out_fmt, log_box, root, conversion_done),
                         daemon=True)
    t.start()

def conversion_done(out_paths, error):
    if error:
        append_log(log_box, f"Error: {error}")
        messagebox.showerror("Conversion failed", error)
    else:
        for p in out_paths:
            append_log(log_box, f"Finished: {p}")
        messagebox.showinfo("Success", f"Converted {len(out_paths)} file(s) → {OUTPUT_DIR}")
        last_output_paths.clear()
        last_output_paths.extend(out_paths)
        open_btn.config(state=NORMAL)
    convert_btn.config(state=NORMAL)

def open_output():
    folder = str(OUTPUT_DIR)
    try:
        if sys.platform.startswith("darwin"):
            subprocess.run(["open", folder])
        elif os.name == "nt":
            os.startfile(folder)
        else:
            subprocess.run(["xdg-open", folder])
    except Exception:
        webbrowser.open("file://" + os.path.abspath(folder))

# Run
root.mainloop()
