import shutil
import subprocess
from pathlib import Path
from .base import Converter
from typing import Dict

class AudioConverter(Converter):
    name = "Audio Converter"
    info = "Audio conversion requires ffmpeg installed and available in PATH."
    input_formats = ["mp3", "wav", "ogg", "flac", "aac", "m4a", "wma"]
    output_formats = ["mp3", "wav", "ogg", "flac", "aac", "m4a", "wma"]

    def __init__(self):
        self.ffmpeg_path = shutil.which("ffmpeg")
        if not self.ffmpeg_path:
            self.ffmpeg_available = False
        else:
            self.ffmpeg_available = True

    def convert(self, input_file: str, output_format: str, options: Dict) -> str:
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not found. Install FFmpeg to use the Audio Converter.")

        input_path = Path(input_file)
        output_path = input_path.with_suffix(f".{output_format}")

        cmd = [
            self.ffmpeg_path,
            "-y",  # overwrite output
            "-i", str(input_path),
            str(output_path)
        ]

        # Run FFmpeg
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")

        return str(output_path)
