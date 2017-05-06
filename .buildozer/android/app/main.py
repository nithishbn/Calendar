import sqlite3
import datetime
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.scrollview import ScrollView
from argon2 import PasswordHasher
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.list import ILeftBodyTouch
from kivymd.theming import ThemeManager
# from kivymd.icon_definitions import

class LoginScreen(Screen):
    def register(self):
        self.manager.current = "RegisterScreen"

    def on_enter(self, *args):
        super().on_enter(*args)
        print("Login")

    def onBackBtn(self, **kwargs):
        super(LoginScreen, self).onBackBtn(**kwargs)
        return 0

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        if len(username) == 0:
            # self.ids.password.error = True
            self.ids.username.error = True
        else:  # username exists in textbox
            conn = sqlite3.connect("data.sqlite")
            cur = conn.cursor()

            try:
                cur.execute('''SELECT Hash from Main WHERE Username = ?''', (username,))
                returnedhash = cur.fetchone()[0]
                p = PasswordHasher()
                isitquestion = p.verify(returnedhash, password)
                if isitquestion:
                    self.manager.current = "MenuScreen"
            except:
                self.ids.password.error = True

class RegisterScreen(Screen):
    def register(self):
        print("Wow well played!")
        return True
        # TODO finish this lol
    def cancel(self):
        self.ids.email.text = ""
        self.ids.phone_number.text = ""
        self.ids.register_password.text = ""
        self.manager.current = "LoginScreen"

class MenuScreen(Screen):
    screenlist = ListProperty([])

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        # self.screenlist.append("MenuScreen")
        print(self.screenlist)
        Window.bind(on_keyboard=self.onBackBtn)

    def onBackBtn(self, window, key, *args):
        if key == 27:
            print("onBackBtn function call", self.screenlist)
            if self.manager.current == "LoginScreen" or self.manager.current == "RegisterScreen":
                return True
            else:
                if len(self.screenlist) != 0:
                    print("escaping")
                    self.manager.current = self.screenlist[len(self.screenlist) - 1]
                    self.screenlist.pop(len(self.screenlist) - 1)
                    return True
                else:
                    return False

    def on_enter(self):
        super(MenuScreen, self).on_enter()
        self.ids.scrolllabelthing.update_self()

    def on_leave(self, *args):
        self.screenlist.append("MenuScreen")
        print("MenuScreen's list: ", self.screenlist)

class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass
class DateScreen(Screen):
    date = StringProperty('')
    otherdate = StringProperty('')
    screenlist = ListProperty

    def __init__(self, **kwargs):
        screenlist = self.screenlist
        super(DateScreen, self).__init__(**kwargs)

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj
        # print(date_obj)
        dt = datetime.datetime.strptime(str(date_obj), '%Y-%m-%d')
        # print("dt", dt)
        actualdate = '{0}/{1}/{2:02}'.format(dt.month, dt.day, dt.year % 100)
        # print(actualdate)
        # print(self.previous_date)
        self.ids.datething.text = actualdate
        self.date = str(actualdate)
        # self.root.ids.date_picker_label.text = str(date_obj)

    def show_date_picker(self):
        MDDatePicker(self.set_previous_date).open()
    def selectdate(self):
        # self.date = self.ids.datething.text
        if self.manager.current not in self.screenlist:
            self.screenlist.append(self.manager.current)
        # print("date selection", self.screenlist)
        self.manager.current = "TodayScreen"

    def figuretime(self):
        dt = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
        actualdate = '{0}/{1}/{2:02}'.format(dt.month, dt.day, dt.year % 100)
        return actualdate


class ConstructionScreen(Screen):
    screenlist = ListProperty([])


class TodayScreen(Screen):
    # screenlist = ListProperty([])
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasae = StringProperty('')
    pakshae = StringProperty('')
    thithi = StringProperty('')
    date = StringProperty('')
    screenlist = ListProperty([])

    # def __init__(self, **kwargs):
    #     super(TodayScreen, self).__init__(**kwargs)
    #     Window.bind(on_keyboard=self.onBackBtn)

    def search(self):
        date = self.date
        # print(date)
        conn = sqlite3.connect('calendar.sqlite')
        cur = conn.cursor()
        try:
            cur.execute(
                '''SELECT date, S.Name, A.Name, R.Name, M.Name, P.Name, V.Name, T.Name FROM Main JOIN Samvatsaram S on Main.samvatsaram = S.SID JOIN Ayanam A on Main.ayanam = A.AID JOIN Rithu R on Main.rithu = R.RID JOIN Maasae M on Main.maasa = M.MID JOIN Pakshae P on Main.pakshae = P.PID JOIN Vaaram V on Main.Vaaram = V.VID JOIN Thithi T on Main.thithi = T.TID WHERE date = ?''',
                (date,))
            thing = cur.fetchone()
            print(thing)
            for query in thing:
                if query == thing[0]:
                    # print("Date:", query)
                    pass
                elif query == thing[1]:
                    # print("Samvatsaramam:", query)
                    self.samva = query
                elif query == thing[2]:
                    # print("Ayanam:", query)
                    self.avanam = query
                elif query == thing[3]:
                    # print("Rithu:", query)
                    self.rithu = query
                elif query == thing[4]:
                    # print("Maasae:", query)
                    self.maasae = query
                elif query == thing[5]:
                    # print("Pakshae:", query)
                    self.pakshae = query
                elif query == thing[6]:
                    # print("Day:", query)
                    pass
                elif query == thing[7]:
                    # print("Thithi:", query)
                    self.thithi = query
        except:
            self.manager.current = "DateScreen"
            # self.ids.datething.text = " "


class ScrollLabel(ScrollView):
    # DONT TOUCH THIS
    def __init__(self, **kwargs):

        super(ScrollLabel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_self)
        Clock.schedule_interval(self.update_self, 2.5)

    def update_self(self, *args):
        if self.scroll_x == 0:
            marquee = Animation(scroll_x=1.0, duration=10.0)
            marquee.start(self)
        elif self.scroll_x >= 0.99:
            self.scroll_x = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return 0


# class ScreenManager(ScreenManager):
#     def toggle_nav_drawer(self):
#         self.toggle_state()
class InterfaceApp(App):
    theme_cls = ThemeManager()
    title = "SVETA Temple"

    def build(self):
        # print(self.theme_cls.
        self.theme_cls.theme_style = 'Dark'

    def on_pause(self):
        return True


if __name__ == '__main__':
    InterfaceApp().run()