from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


################################################################################
class ExampleRoot(BoxLayout):
    """ Root widget for app """
    screen_manager = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(ExampleRoot, self).__init__(*args, **kwargs)
        # list to keep track of screens we were in
        self.list_of_prev_screens = []

    # --------------------------------------------------------------------------
    def onNextScreen(self, btn, next_screen):
        # add screen we were just in
        self.list_of_prev_screens.append(btn.parent.name)
        # Go to next screen
        self.screen_manager.current = next_screen

    def onBackBtn(self):
        # Check if there are any screens to go back to
        if self.list_of_prev_screens:
            # If there are then just go back to it
            self.screen_manager.current = self.list_of_prev_screens.pop()
            # We don't want to close app
            return True
        # No more screens so user must want to exit app
        return False

################################################################################
class ExampleApp(App):
    """ App to show how to use back button """

    def __init__(self, *args, **kwargs):
        super(ExampleApp, self).__init__(*args, **kwargs)

    # --------------------------------------------------------------------------
    def build(self):
        return ExampleRoot()

    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc key """
        # 27 is back press number code
        if key == 27:
            # Call the "OnBackBtn" method from the "ExampleRoot" instance
            return self.root.onBackBtn()
        return False

if __name__ == "__main__":
    ExampleApp().run()