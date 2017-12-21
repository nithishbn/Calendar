import sqlite3
import datetime
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, ListProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.date_picker import MDDatePicker
from kivymd.theming import ThemeManager
from plyer import call
import os
from passlib.hash import argon2


class LoginScreen(Screen):
    count = 0

    def register(self):
        self.manager.current = "RegisterScreen"

    def on_enter(self, *args):
        super(LoginScreen, self).on_enter(*args)
        if self.count > 0:
            self.ids.username.error = False
            self.ids.username.text = ''
            self.ids.password.error = False
            self.ids.password.text = ''

    def onBackBtn(self, **kwargs):
        super(LoginScreen, self).onBackBtn(**kwargs)
        return 0

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        # self.manager.current = "MenuScreen"
        if len(username) == 0:
            self.ids.username.error = True
            self.ids.username.focus = False
            self.ids.username.focus = True
        else:  # username exists in textbox
            conn = sqlite3.connect("data.sqlite")
            cur = conn.cursor()
            try:
                cur.execute('''SELECT Hash FROM users WHERE Username = ?''', (username,))
                returnedhash = cur.fetchone()[0]

                isitquestion = argon2.verify(password, returnedhash)
                if isitquestion:
                    self.manager.current = "MenuScreen"
            except:
                self.ids.password.error = True
                self.ids.password.focus = True
                self.ids.password.focus = False


class RegisterScreen(Screen):
    emailvar = StringProperty('')
    phonevar = StringProperty('')
    usernamevar = StringProperty('')

    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.count = 0
        self.conn = sqlite3.connect("data.sqlite")
        self.cur = self.conn.cursor()
        self.ids.email.bind(text=self.settext)
        self.ids.phone_number.bind(text=self.settext)
        self.ids.usernameregister.bind(text=self.settext)

    def settext(self, *args):
        # if args == 'email':
        # print(self.count)
        self.emailvar = self.ids.email.text
        self.phonevar = self.ids.phone_number.text
        self.usernamevar = self.ids.usernameregister.text
        if self.count == 0:
            if len(self.ids.email.text) == 0:
                self.ids.email.error = False
            else:
                # print(str(self.emailvar))
                self.cur.execute('''SELECT key FROM users WHERE Email = ?''', (self.emailvar,))
                results = self.cur.fetchall()
                # print(results)
                if len(results) == 0:
                    self.ids.email.error = False
                    self.ids.email.focus = False
                    self.ids.email.focus = True
                elif len(results) != 0:
                    self.ids.email.error = True
                    self.ids.email.focus = False
                    self.ids.email.focus = True
        elif self.count > 0:

            if len(self.ids.phone_number.text) == 0:
                self.ids.phone_number.error = False
            else:
                self.cur.execute('''SELECT key FROM users WHERE Phone = ?''', (str(self.phonevar),))
                results2 = self.cur.fetchall()
                if len(results2) == 0:
                    self.ids.phone_number.error = False
                    self.ids.phone_number.focus = False
                    self.ids.phone_number.focus = True
                elif len(results2) != 0:
                    self.ids.phone_number.error = True
                    self.ids.phone_number.focus = False
                    self.ids.phone_number.focus = True
        elif self.count < 0:
            if len(self.ids.usernameregister.text) == 0:
                self.ids.usernameregister.error = False
                self.ids.usernameregister.focus = False
                self.ids.usernameregister.focus = True
            else:
                self.cur.execute('''SELECT key FROM users WHERE Username = ?''', (str(self.usernamevar),))
                results3 = self.cur.fetchall()
                if len(results3) == 0:
                    self.ids.usernameregister.error = False
                    self.ids.usernameregister.focus = False
                    self.ids.usernameregister.focus = True
                elif len(results3) != 0:
                    print(self.usernamevar)
                    self.ids.usernameregister.error = True
                    self.ids.usernameregister.focus = False
                    self.ids.usernameregister.focus = True

    def register(self):
        self.conn = sqlite3.connect("data.sqlite")
        self.cur = self.conn.cursor()
        email = self.ids.email.text
        phone = self.ids.phone_number.text
        password = self.ids.register_password.text
        verify = self.ids.verify.text
        register = argon2.hash(self.ids.register_password.text)
        if not argon2.verify(verify, register):
            self.ids.verify.error = True
            self.ids.register_password.error = True
        else:
            self.ids.verify.error = False
            self.ids.register_password.error = False

        if self.ids.verify.error or self.ids.register_password.error or self.ids.email.error or self.ids.usernameregister.error or self.ids.phone_number.error:
            print(self.ids.verify.error)
            print(self.ids.register_password.error)
            print(self.ids.email.error)
            print(self.ids.usernameregister.error)
            print(self.ids.phone_number.error)
            print("fail")
        else:
            self.cur.execute(
                '''INSERT INTO users (Username, Hash, Email, Phone) VALUES ("{}","{}","{}","{}")'''.format(
                    self.ids.usernameregister.text, register, self.ids.email.text, self.ids.phone_number.text))
            self.conn.commit()
            self.ids.verify.text = ''
            self.ids.register_password.text = ''
            self.ids.phone_number.text = ''
            self.ids.usernameregister.text = ''
            self.ids.email.text = ''
            self.emailvar = ''
            self.phonevar = ''
            self.usernamevar = ''
            self.manager.current = "LoginScreen"

    def cancel(self):
        self.ids.email.text = ""
        self.ids.phone_number.text = ""
        self.ids.register_password.text = ""
        self.ids.verify.text = ''
        self.ids.usernameregister.text = ''
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


class DateScreen(Screen):
    date = StringProperty('')
    otherdate = StringProperty('')
    screenlist = ListProperty
    count = 0

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
        self.count -= 1
        self.selectdate()
        # self.root.ids.date_picker_label.text = str(date_obj)

    def show_date_picker(self):
        # self.focus = False
        if self.count == 0:
            self.count += 1
            MDDatePicker(self.set_previous_date).open()
            # self.count -= 1
        else:
            return True
            # MDDatePicker(self.set_previous_date).open()

    def selectdate(self):
        # self.date = self.ids.datething.text
        print(self.ids.datething.text)
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


class GalleryScreen(Screen):
    screenlist = ListProperty([])
    imagefile = StringProperty("./images/2014-10-01-01.00.23.jpg")
    filenames = ListProperty([])
    count = NumericProperty(0)
    lengthoflist = NumericProperty()

    def on_enter(self, *args):
        print(self.manager)
        self.count = 0
        self.filenames = []
        for file in os.listdir("./images"):
            self.filenames.append("./images/" + file)
        self.lengthoflist = len(self.filenames)
        self.imagefile = self.filenames[0]
        self.count += 1

    def next_image(self):
        self.imagefile = self.filenames[self.count]
        print(self.count)
        self.count += 1
        if self.count == len(self.filenames):
            self.count = 0

    def previous_image(self):
        self.imagefile = self.filenames[self.count]
        self.count -= 1
        if self.count < 0:
            self.count = len(self.filenames) - 1


class ContactScreen(Screen):
    screenlist = ListProperty([])

    def on_enter(self, *args):
        super(ContactScreen, self).on_enter(*args)

    def call(self):
        call.makecall(tel="12062195330")


# call.dialcall()
class TodayScreen(Screen):
    # screenlist = ListProperty([])
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasae = StringProperty('')
    pakshae = StringProperty('')
    thithi = StringProperty('')
    vara = StringProperty('')
    date = StringProperty('')
    screenlist = ListProperty([])

    # DO NOT TOUCH THIS AT ALL
    # if you do, you will be decimated by Nithish Narasimman idk though
    def search(self):
        date = self.date
        print("search date function thing: ", date)
        # print(date)
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()
        try:
            cur.execute(
                '''SELECT date, S.Name, A.Name, R.Name, M.Name, P.Name, V.Name, T.Name FROM Calendar JOIN Samvatsaram S ON Calendar.samvatsaram = S.SID JOIN Ayanam A ON Calendar.ayanam = A.AID JOIN Rithu R ON Calendar.rithu = R.RID JOIN Maasae M ON Calendar.maasa = M.MID JOIN Pakshae P ON Calendar.pakshae = P.PID JOIN Vaaram V ON Calendar.Vaaram = V.VID JOIN Thithi T ON Calendar.thithi = T.TID WHERE date = ?''',
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
                    self.vara = query
                elif query == thing[7]:
                    # print("Thithi:", query)
                    self.thithi = query
        except:
            print("wat")
            self.manager.current = "DateScreen"
            # self.app.ids.datething.error = True
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
        # self.theme_cls.theme_style = 'Dark'
        pass

    def on_pause(self):
        return True


if __name__ == '__main__':
    InterfaceApp().run()
