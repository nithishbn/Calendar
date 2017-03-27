from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             OptionProperty, ObjectProperty, StringProperty)
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

Builder.load_string("""
<AutoScrollableVLabel>:
    label: __label
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: (self.width, None)

        id: __label
        text: root.text
        font_name: root.font_name
        font_size: root.font_size
        line_height: root.line_height
        bold: root.bold
        italic: root.italic
        halign: root.halign
        valign: root.valign
        color: root.color
        max_lines: root.max_lines

<AutoScrollableHLabel>:
    label: __label
    Label:
        size_hint_x: None
        height: root.height
        width: self.texture_size[0]

        id: __label
        text: root.text
        font_name: root.font_name
        font_size: root.font_size
        line_height: root.line_height
        bold: root.bold
        italic: root.italic
        halign: root.halign
        valign: root.valign
        color: root.color
        max_lines: root.max_lines
""")


class AutoScrollableLabel(object):
    label = ObjectProperty(None)
    autoscroll = BooleanProperty(True)
    duration = NumericProperty(10)
    duration = BooleanProperty(False)
    delay = NumericProperty(1)
    text = StringProperty('')
    font_name = StringProperty('Roboto')
    font_size = NumericProperty('15sp')
    line_height = NumericProperty(1.0)
    bold = BooleanProperty(False)
    italic = BooleanProperty(False)
    color = ListProperty([1, 1, 1, 1])
    max_lines = NumericProperty(0)
    orientation = OptionProperty('vertical', options=['horizontal', 'vertical', 'oneline'])
    valign = OptionProperty('bottom', options=['bottom', 'middle', 'top'])
    halign = OptionProperty('left', options=['left', 'center',
                                             'right', 'justify'])

    l_size_hint_x = NumericProperty(1, allownone=True)
    l_size_hint_y = NumericProperty(1, allownone=True)

    def on_autoscroll(self, instance, scroll):
        if scroll:
            Clock.schedule_once(self.do_scroll, self.delay)

    def do_scroll(self, *args):
        if self.orientation == 'vertical':
            anim = Animation(scroll_y=0, duration=self.duration)
        else:
            anim = Animation(scroll_x=1, duration=self.duration)
        anim.start(self)

    def on_text(self, instance, text):
        if self.autoscroll:
            Clock.schedule_once(self.do_scroll, self.delay)


class AutoScrollableVLabel(AutoScrollableLabel, ScrollView):

    def __init__(self, **kwargs):
        super(AutoScrollableVLabel, self).__init__(**kwargs)
        self.orientation = 'vertical'


class AutoScrollableHLabel(AutoScrollableLabel, ScrollView):

    def __init__(self, **kwargs):
        self.orientation = 'horizontal'
        super(AutoScrollableHLabel, self).__init__(**kwargs)
