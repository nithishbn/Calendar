from kivy.app import App
from kivy.lang import Builder

kv = '''
Widget:
    Button:
        pos: 200, 200
        canvas.before:
            BorderImage:
                source: 'tex.png'
                pos: self.x - 50, self.y - 50
                size: self.width + 100, self.height + 100
'''


class MyApp(App):
    def build(self):
        return Builder.load_string(kv)


MyApp().run()
