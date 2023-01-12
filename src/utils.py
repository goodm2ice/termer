from PIL import Image
from io import BytesIO
from typing import Callable, List, Optional, TypeVar
from customtkinter import CTkImage


def blob_to_image(blob, max_width: Optional[int] = None, max_height: Optional[int] = None):
    if not blob: return None
    img = Image.open(BytesIO(blob))

    k = img.width / img.height
    size = None
    if type(max_width) == int and max_width > 0:
        size = (max_width, int(max_width / k))
    if (type(max_height) == int and max_height > 0) and (not size or size[1] > max_height):
        size = (int(max_height * k), max_height)

    return CTkImage(dark_image=img, size=size)


T = TypeVar('T')
def find(arr: List[T], expression: Callable[[T, int, List[T]], bool]) -> T | None:
    for i, elm in enumerate(arr):
        if expression(elm, i, arr):
            return elm
    return None
