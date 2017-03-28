from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
Builder.load_string('''
<Spacer@Widget>:
    size_hint_x: None
    width: 800

<ScrollLabel>:
    GridLayout:
        rows: 1
        size_hint_x: None
        width: self.minimum_width
        Spacer:
        Label:
            size_hint_x: None
            text: 'Nithish is the best'
            width: self.texture_size[0]
        Spacer:

''')
class ScrollLabel(ScrollView): pass
scroll = ScrollLabel(scroll_y=-1)
marquee = Animation(scroll_x=1, duration=5)

marquee.repeat = True
marquee.start(scroll)
runTouchApp(scroll)