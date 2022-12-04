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

from .utils import flatten
from .text_to_image import Bitmap, Font as _Font

from PIL import Image


FONT_PATH = Path(__file__).parent.parent / "fonts"


class Face(Enum):
    """typeface"""
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
    """face + size = font"""
    face: Face | str
    size: int

    @property
    def face_str(self) -> str:
        if isinstance(self.face, Face):
            return self.face.value
        return self.face

    def _render(self, text) -> Bitmap:
        _fnt = _load_font(self)
        return _fnt.render_text(text)

    def to_str(self, text: str) -> str:
        """convert to string"""
        return str(self._render(text))

    def to_image(
        self,
        text: str,
        *,
        color: Color = Color.parse("yellow"),
        height: Optional[int] = None,
    ) -> Image.Image:
        """convert to PIL image"""
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
        """convert to an object that is renderable by rich"""
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
