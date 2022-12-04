from random import sample
from typing import Optional

from rich import print
from rich.emoji import Emoji, EMOJI
from rich.table import Table
from rich import print

from text_to_image import Font, Face


def _get_inconsistent_width_emoji() -> set[str]:
    """emoji have variable widths and are tough to use with spaces
    to make something readable

    return a set of these
    """

    def _inconsistent_width(n):
        return n.startswith(("flag_for", "regional_indicator")) or n.endswith(
            "skin_tone"
        )

    return {e for name, e in EMOJI.items() if _inconsistent_width(name)}


def _init_good_emoji():
    """create a list of "good" emoji - i.e. ones that work well with spaces"""
    return list(set(EMOJI.values()) - _get_inconsistent_width_emoji())


_good_emoji = _init_good_emoji()


def random_emoji(n=1) -> str:
    """get `n` "good" emoji as a str"""
    return "".join(sample(_good_emoji, n))


def _convert_bits(bits: list[list[int]], emoji: str, flip: bool) -> list[str]:
    """flip bits based on `flip` and convert to emojified strings"""
    return ["".join(emoji if flip ^ v else "  " for v in row) for row in bits]


def _with_border(bits) -> list[list[int]]:
    """add blank bits around "image" to make it easier to read"""
    width = len(bits[0]) + 2

    res = [[0] * width]
    res.extend([0, *v, 0] for v in bits)
    res.append([0] * width)
    return res


def emojify_text(
    text: str,
    emoji: Optional[str] = None,
    font: Font = Font(Face.courier_new, 13),
    flip: bool = False,
) -> str:
    """turn one line of text into an emoji str

    the idea is convert text -> bitmap, replace each of the bits
    with an emoji, then return the str of that
    """
    emoji = emoji or random_emoji()
    if emoji.isascii():
        emoji = str(Emoji(emoji.strip(":")))

    bits = font._render(text).bits
    bits = _with_border(bits)
    return "\n".join(_convert_bits(bits, emoji, flip))


def display_emoji(s="") -> None:
    """display all available emoji"""
    for name, emoji in EMOJI.items():
        if s in name:
            print(emoji, name)


def explore_emojify_text(
    text, emoji="exploding_head", size_range=range(11, 16), faces=tuple(Face)
) -> None:
    """see how different faces/sizes look
    
    display with rich.print
    """
    t = Table("typeface", "size", "text", width=175)

    def store_row(*args, **kwargs):
        temp.append((args, kwargs))

    temp = [((), {})]
    for s in size_range:
        temp[-1][1]["end_section"] = True
        for f in faces:
            store_row()
            res = emojify_text(text, emoji=emoji, font=Font(f, size=s), flip=False)
            store_row(f.name, str(s), res)
            store_row()
    for a, kw in temp[1:]:
        t.add_row(*a, **kw)
    return print(t)


def __main():
    print(random_emoji())
    print(emojify_text("jygify", flip=False, font=Font(Face.comic_sans, 13)))


if __name__ == "__main__":
    __main()
