from PIL import Image
from .base import Converter
from typing import Dict
from pathlib import Path

class ImageConverter(Converter):
    name = "Image Converter"
    
    input_formats = ["jpg", "jpeg", "png", "bmp", "gif"]
    output_formats = ["jpg", "jpeg", "png", "bmp", "gif"]

    FORMAT_MAP = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "bmp": "BMP",
        "gif": "GIF",
    }

    def convert(self, input_file: str, output_format: str, options: Dict) -> str:
        input_path = Path(input_file)   # normalize
        outdir = Path(options.get("output_dir", input_path.parent))
        outdir.mkdir(parents=True, exist_ok=True)

        output_path = outdir / f"{input_path.stem}.{output_format.lower()}"
        out_format = self.FORMAT_MAP[output_format.lower()]

        with Image.open(input_path) as img:
            # JPEG handling (no alpha)
            if out_format == "JPEG" and img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                alpha_channel = img.split()[-1]
                background.paste(img, mask=alpha_channel)
                img = background

            # GIF handling (ensure palette/transparency)
            elif out_format == "GIF":
                if img.mode in ("RGBA", "LA"):
                    alpha = img.convert("RGBA").split()[-1]
                    img = img.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
                    img.info["transparency"] = 255
                elif img.mode != "P":
                    img = img.convert("P", palette=Image.ADAPTIVE)

            # Palette images (other formats)
            elif img.mode == "P":
                img = img.convert("RGB")
            elif img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            img.save(output_path, format=out_format)

        return str(output_path)
