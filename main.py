import sqlite3
import datetime
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, ListProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.date_picker import MDDatePicker
from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar
from plyer import call
import os


class Navigation(NavigationLayout):
    pass


class MenuScreen(Screen):
    screenlist = ListProperty()

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        print(self.screenlist)

        Window.bind(on_keyboard=self.onBackBtn)

    def onBackBtn(self, window, key,*args):
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

    def on_leave(self, *args):
        self.screenlist.append("MenuScreen")
        print("MenuScreen's list: ", self.screenlist)


class DateScreen(Screen):
    date = StringProperty('')
    otherdate = StringProperty('')
    screenlist = ListProperty()
    count = 0

    def __init__(self, **kwargs):
        # screenlist = self.screenlist
        super(DateScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.show_date_picker()

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj
        dt = datetime.datetime.strptime(str(date_obj), '%Y-%m-%d')
        actualDate = '{0}-{1}-{2}'.format(dt.day, dt.strftime("%b"), dt.year % 100)
        self.date = str(actualDate)
        self.selectdate()

    def show_date_picker(self):
        if self.count != -1:
            MDDatePicker(self.set_previous_date).open()
            # self.count -= 1
        else:
            print("nope")
            return True
            # MDDatePicker(self.set_previous_date).open()

    def selectdate(self):
        if self.manager.current not in self.screenlist:
            self.screenlist.append(self.manager.current)
        self.manager.current = "TodayScreen"


class ConstructionScreen(Screen):
    screenlist = ListProperty()


class GalleryScreen(Screen):
    screenlist = ListProperty()
    imagefile = StringProperty("./images/2014-10-01-01.00.23.jpg")
    filenames = ListProperty()
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
    screenlist = ListProperty()

    def on_enter(self, *args):
        super(ContactScreen, self).on_enter(*args)

    def call(self):
        call.makecall(tel="12062195330")


# call.dialcall()
class TodayScreen(Screen):
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasae = StringProperty('')
    pakshae = StringProperty('')
    thithi = StringProperty('')
    vara = StringProperty('')
    date = StringProperty('')
    screenlist = ListProperty()
    count = NumericProperty()

    def on_pre_enter(self, *args):
        self.count = 0
        success = self.search()
        if success == -1:
            self.count += 1
            self.manager.current = "DateScreen"

    # DO NOT TOUCH THIS AT ALL
    # if you do, you will be decimated by Nithish Narasimman idk though

    def search(self):
        date = self.date
        print("search date function thing: ", date)
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()

        cur.execute(
            '''SELECT
Date,
S.Samvatsaram,
A.Ayanam,
R.Rithu,
M.TamilMaasa,
V.Vaaram,
T.Thithi,
N.Nakshatra,
C.Notes1,
C.Notes2,
C.Notes3,
C.Notes4
FROM Calendar2018 C, Samvatsaram S, Ayanam A, Rithu R, TamilMaasa M, Vaaram V, Thithi T, Nakshatra N
WHERE date = ? AND S.ID =
                        C.samvatsaram AND A.ID = C.ayanam AND R.ID = C.rithu AND M.ID = C.TamilMaasa AND
  V.ID = C.vaaram AND T.ID = C.Thithi1 AND N.ID = C.Nakshtra1''',
            (date,))
        thing = cur.fetchone()
        print(thing)
        if thing is None:
            return -1
        else:
            for query in thing:
                if query == thing[1]:
                    self.samva = query
                elif query == thing[2]:
                    self.avanam = query
                elif query == thing[3]:
                    self.rithu = query
                elif query == thing[4]:
                    self.maasae = query
                elif query == thing[5]:
                    self.pakshae = query
                elif query == thing[6]:
                    self.vara = query
                elif query == thing[7]:
                    self.thithi = query


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
