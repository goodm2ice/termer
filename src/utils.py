from PIL import Image, ImageTk
from io import BytesIO
from typing import Optional


def blob_to_image(blob, max_width: Optional[int] = None, max_height: Optional[int] = None):
    if not blob: return None
    img = Image.open(BytesIO(blob))

    has_w = type(max_width) == int and max_width > 0
    has_h = type(max_height) == int and max_height > 0

    if has_w and has_h:
        img.resize((max_width, max_height))
    elif has_w:
        img.resize((max_width, max_width / img.width * img.height))
    elif has_h:
        img.resize((max_height / img.height * img.width, max_height))

    return ImageTk.PhotoImage(img)
