from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from newuser import newuser

class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.add_widget(Label(text='User Name', size_hint_y=None))
        self.username = TextInput(size_hint_y=None,multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password', size_hint_y=None))
        self.password = TextInput(password=True, size_hint_y=None,multiline=False)
        self.add_widget(self.password)



class MyApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()