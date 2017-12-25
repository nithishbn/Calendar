import sqlite3
import datetime
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, ListProperty, NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivymd.date_picker import MDDatePicker
from kivymd.navigationdrawer import NavigationLayout

from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar
from plyer import call
import os
# from passlib.hash import argon2


class Navigation(NavigationLayout):
    pass


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

    def on_enter(self, *args):
        super(MenuScreen, self).on_enter()
        print(self.ids)
        # self.scrolllabelthing.update_self()

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

    def on_pre_enter(self, *args):
        self.search()

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

class AToolbar(Toolbar):
    pass
class InterfaceApp(App):
    theme_cls = ThemeManager()
    title = "SVETA Temple"

    def build(self):
        pass

    def on_pause(self):
        return True


if __name__ == '__main__':
    InterfaceApp().run()
