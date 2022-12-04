from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import groupby
import string

from enum import Enum
from pathlib import Path
from typing import NamedTuple, Optional
from rich.color import Color
from rich.color_triplet import ColorTriplet
from rich.style import Style
from rich.segment import Segment
from rich.text import Text

from .utils import flatten
from .text_to_bitmap import Bitmap, Font as _Font

from PIL import Image


FONT_PATH = Path(__file__).parent.parent / "fonts"


class Face(Enum):
    typewriter = "AmericanTypewriter.ttc"
    comic_sans = "Comic Sans MS.ttf"
    courier_new = "Courier New.ttf"
    futura = "Futura.ttc"
    jet_brains_mono = "JetBrainsMono-Light.ttf"
    menlo = "Menlo.ttc"
    papyrus = "Papyrus.ttc"

    def explore(self, size_range: range = range(6, 30)):
        """print out dimensions for a particular face in a range of sizes"""
        face_name = self.value
        print(face_name)
        for size in size_range:
            fnt = _load_font(face_name, size)
            print(size, fnt.text_dimensions(string.printable))
        print(face_name)


class Font(NamedTuple):
    face: Face | str
    size: int

    @property
    def face_str(self) -> str:
        if isinstance(self.face, Face):
            return self.face.value
        return self.face

    def to_str(self, text: str) -> str:
        return str(self._render(text))

    def _render(self, text) -> Bitmap:
        _fnt = _load_font(self)
        return _fnt.render_text(text)

    def to_image(
        self,
        text: str,
        *,
        color: Color = Color.parse("yellow"),
        height: Optional[int] = None,
    ):
        bm = self._render(text).add_border(10)
        triplet = color.get_truecolor()
        colors = bytearray(flatten(triplet if px else (0, 0, 0) for px in bm.pixels))  # type: ignore
        im = Image.frombytes("RGB", (bm.width, bm.height), bytes(colors))
        if height:
            im = _resize_image(im, height)
        return im

    def to_rich(
        self,
        text: str,
        *,
        color: Color = Color.parse("yellow"),
        height: Optional[int] = None,
    ) -> ImageAsText:
        im = self.to_image(text, color=color, height=height)
        return ImageAsText(im)


@dataclass
class ImageAsText:
    im: Image.Image

    def __rich_console__(self, *_):
        """run length encode pixels to segments"""
        pixels = self.im.load()
        matrix = (
            (pixels[c, r] for c in range(self.im.width)) for r in range(self.im.height)
        )
        groups = (
            ((rgb, sum(1 for _ in v)) for rgb, v in groupby(row)) for row in matrix
        )
        for row in groups:
            for rgb, length in row:
                style = Style(bgcolor=_rgb_to_color(rgb))
                yield Segment(" " * length, style)
            yield Segment("\n")


def _rgb_to_color(pixel) -> Color:
    return Color.from_triplet(ColorTriplet(*pixel))


def _resize_image(im: Image.Image, height: int) -> Image.Image:
    """keep image proportional but resize"""
    return im.resize((int(im.width * height / im.height), height), Image.ANTIALIAS)


@lru_cache(8)
def _load_font(font: Font) -> _Font:
    return _Font(f"{FONT_PATH}/{font.face_str}", font.size)


# def will_help_with_rich():
#     res = [80 * '=', f'ColorMatrix: Shape{self.shape}']
#     # run length encode groups with (color, num_repeats) tuples for less overhead
#     groups = (((c, sum(1 for _ in v)) for c, v in groupby(row)) for row in self)
#     res.extend(
#         ''.join(c.color_str('  ' * total, set_bg=True) for c, total in row) for row in groups
#     )
#     res.append(80 * '=')
#     res.append('')
#     return '\n'.join(res)


# def resize(self, shape: Shape = (8, 8)) -> 'ColorMatrix':
#     """resize image using pillow and return a new ColorMatrix"""
#     if self.shape == shape:
#         return self.copy()

#     im = Image.new('RGB', self.shape, 'black')
#     pixels = im.load()
#     for c, r in product(range(im.width), range(im.height)):
#         with suppress(IndexError):
#             pixels[c, r] = self[r][c].rgb[:3]

#     y, x = shape
#     im = im.resize((x, y), Image.ANTIALIAS)
#     pixels = im.load()
#     res = ColorMatrix.from_shape(shape)

#     for c, r in product(range(im.width), range(im.height)):
#         with suppress(IndexError):
#             res[r][c] = pixels[c, r]

#     return res.cast(lambda rgb: Color.from_rgb(RGBk(*rgb)))
