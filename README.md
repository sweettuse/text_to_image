# text_to_image
convert text to bitmaps, images, rich, etc

it's kinda hard to take plain text and render it in a font as an image. this helps with that.

(hat tip to @dbader for the hard part - i just added the fun stuff)

so, e.g. 

```python
from text_to_image import Face, Font, emojify_text, explore_emojify_text
from rich import print
from rich.color import Color

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
```
<img width="1620" alt="Screen Shot 2022-12-04 at 12 20 29 PM" src="https://user-images.githubusercontent.com/3999008/205505598-d06b394a-6a56-47c9-9269-6aba8c4fcbb7.png">
<img width="962" alt="Screen Shot 2022-12-04 at 12 21 18 PM" src="https://user-images.githubusercontent.com/3999008/205505629-5c83a976-bf41-43d1-a923-e2577c62f937.png">
