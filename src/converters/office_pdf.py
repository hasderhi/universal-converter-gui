import subprocess
from pathlib import Path
from .base import Converter
from typing import Dict
import shutil
import os

class OfficeToPDFConverter(Converter):
    name = "Office to PDF"
    input_formats = ["doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp"]
    output_formats = ["pdf"]

    info = "LibreOffice is required for Office to PDF conversion. Make sure LibreOffice is installed, otherwise conversion will fail. You can download LibreOffice from: https://www.libreoffice.org/"

    def __init__(self):
        # First try PATH
        self.libreoffice_path = shutil.which("soffice")

        # If not found, try typical Windows install locations
        if not self.libreoffice_path:
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    self.libreoffice_path = p
                    break

        self.available = bool(self.libreoffice_path)

    def convert(self, input_file: str, output_format: str, options: Dict) -> str:
        if not self.available:
            raise RuntimeError("LibreOffice not found. Install it or add it to PATH to enable Office->PDF conversion.")

        input_path = Path(input_file)
        output_dir = input_path.parent

        cmd = [
            self.libreoffice_path,
            "--headless",
            "--convert-to", output_format,
            "--outdir", str(output_dir),
            str(input_path)
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"LibreOffice conversion failed: {e.stderr.decode()}")

        output_file = input_path.with_suffix(f".{output_format}")
        if not output_file.exists():
            raise RuntimeError("Conversion failed, output file not found.")

        return str(output_file)
