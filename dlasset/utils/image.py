"""Utility functions for image processing."""
from PIL import Image

__all__ = ("merge_y_cb_cr_a", "crop_image")


def merge_y_cb_cr_a(img_y: Image, img_cb: Image, img_cr: Image, img_alpha: Image) -> Image:
    """Merge the image channel of YCbCr and alpha into one single image."""
    y = img_y.split()[-1]  # Y uses A for value
    cb = img_cb.convert("L").resize(y.size, Image.ANTIALIAS)
    cr = img_cr.convert("L").resize(y.size, Image.ANTIALIAS)

    img = Image.merge("YCbCr", (y, cb, cr)).convert("RGBA")

    a = img_alpha.convert("L")

    img.putalpha(a)

    return img


def crop_image(img: Image, x: int, y: int, w: int, h: int) -> Image:
    """Crop ``img`` starting from the top-left corner at ``(x, y)`` with size ``w x h``."""
    return img.crop((x, y, w, h))
