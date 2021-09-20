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


def crop_image(img: Image, tl_x: int, tl_y: int, rb_x: int, rb_y: int) -> Image:
    """Crop ``img`` starting from the top-left corner at ``(tl_x, tl_y)`` to the right-bottom at ``(rb_x, rb_y)``."""
    return img.crop((tl_x, tl_y, rb_x, rb_y))
