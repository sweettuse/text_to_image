from text_to_image import Face, Font, emojify_text, explore_emojify_text
from rich import print
from rich.color import Color

print()
# simple terminal str
print(Font(Face.menlo, 12).to_str('hello'))

# with color using rich
print(Font(Face.menlo, 12).to_rich('hello', color=Color.parse('purple')))

# emojify text
print(emojify_text('what a great font', font=Font(Face.comic_sans, 12), emoji='saxophone'))

# emojify text more!
print(emojify_text('what a great font', font=Font(Face.comic_sans, 12), emoji='saxophone', flip=True))

# create an image
im = Font(Face.typewriter, 100).to_image('hello!')
im.show()

print()