from __future__ import annotations

from text_to_image import Face, Font, emojify_text, explore_emojify_text
from rich.color import Color
from rich.color_triplet import ColorTriplet
from rich.segment import Segment
from rich.style import Style
from rich import print
from text_to_image.emoji import emojify_text, explore_emojify_text

def _play():
    # Single characters
    explore_emojify_text('hello', emoji='saxophone')
    print(emojify_text('hi', font=Font(Face.courier_new, 8)))
    fnt = Font(Face.courier_new, 20)
    # print(fnt.to_str('hello'))
    # print(Color.parse('yellow').get_truecolor())
    # print(fnt.to_rich('12:40'))
    # print(fnt.to_rich('10:39'))
    # print(fnt.to_rich('hello', height=40))
    return
    fnt = load_font('Courier New.ttf', 13)
    ch = fnt.render_character('e')

if __name__ == '__main__':
    _play()