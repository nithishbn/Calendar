import sqlite3
from datetime import datetime
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, ListProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBodyTouch
from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar
from plyer import call
import os


class Navigation(NavigationLayout):
    pass


class MenuScreen(Screen):
    screenlist = ListProperty([])
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasa = StringProperty('')
    tmaasa = StringProperty('')
    paksha = StringProperty('')
    thithi = StringProperty('')
    vara = StringProperty('')
    date = StringProperty('')
    nakshatra = StringProperty('')
    nakshatraTime = StringProperty('')
    nakshatra2 = StringProperty('')
    nakshatra2Time = StringProperty('')
    note1 = StringProperty('')
    note2 = StringProperty('')
    note3 = StringProperty('')
    note4 = StringProperty('')

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        print(self.screenlist)

        Window.bind(on_keyboard=self.onBackBtn)

    def search(self):
        date = datetime.today().strftime("%d-%b-%y")
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()

        cur.execute(
            '''SELECT
    Date,
    S.Samvatsaram,
    A.Ayanam,
    R.Rithu,
    M.TamilMaasa,
    TM.TeluguMaasa,
    V.Vaaram,
    T.Thithi,
    N.Nakshatra,
    C.Nakshtra1Time,
    C.Nakshtra2Time,
    C.Notes1,
    C.Notes2,
    C.Notes3,
    C.Notes4
    FROM Calendar2018 C, Samvatsaram S, Ayanam A, Rithu R, TamilMaasa M, TeluguMaasa TM, Vaaram V, Thithi T, Nakshatra N
    WHERE date = ? AND S.ID =
                            C.samvatsaram AND A.ID = C.ayanam AND R.ID = C.rithu AND M.ID = C.TamilMaasa AND TM.ID = C.TeluguMaasa AND
      V.ID = C.vaaram AND T.ID = C.Thithi1 AND N.ID = C.Nakshtra1 ''',
            (date,))
        thing = cur.fetchone()
        print(thing)
        if thing is None:
            print(self.ids)
            self.samva = "null"
            self.avanam = "null"
            self.nakshatraTime = "null"
            self.paksha = "null"
            self.rithu = "null"
            self.maasa = "null"
            self.tmaasa = "null"
            self.vara = "null"
            self.thithi = "null"
            self.nakshatraTime = "null"
            self.nakshatra = "null"
            self.nakshatra2Time = "null"
            self.nakshatra2 = "null"

        else:
            self.samva = thing[1] + " nama samvatsarae"
            self.avanam = thing[2]
            self.rithu = thing[3] + "a rithu"
            self.maasa = "Tamil Maasa: " + thing[4] + " maasae"
            self.tmaasa = "Telugu Maasa: " + thing[5] + " maasae"
            self.paksha = "heehee" + " paksha"
            self.vara = thing[6]
            self.thithi = thing[7] + " thithu"
            self.nakshatraTime = thing[9]
            self.nakshatra = thing[8] + " nakshatra starts at " + self.nakshatraTime
            self.nakshatra2Time = thing[11]
            self.nakshatra2 = thing[10] + " nakshatra starts at " + self.nakshatra2Time

    def onBackBtn(self, window, key, *args):
        if key == 27:
            print("onBackBtn function call", self.screenlist)
            if len(self.screenlist) != 0:
                print("escaping")
                self.manager.current = self.screenlist[len(self.screenlist) - 1]
                self.screenlist.pop(len(self.screenlist) - 1)
                return True
            else:
                return False

    def on_enter(self, *args):
        # with open("used.txt", "r") as file:
        #     used = file.read()
        #
        #     if used == "0":
        #         content = MDLabel(font_style='Body1',
        #                           theme_text_color='Secondary',
        #                           text="Lorem ipsum dolor sit amet, consectetur "
        #                                "adipiscing elit, sed do eiusmod tempor "
        #                                "incididunt ut labore et dolore magna aliqua. "
        #                                "Ut enim ad minim veniam, quis nostrud "
        #                                "exercitation ullamco laboris nisi ut aliquip "
        #                                "ex ea commodo consequat. Duis aute irure "
        #                                "dolor in reprehenderit in voluptate velit "
        #                                "esse cillum dolore eu fugiat nulla pariatur. "
        #                                "Excepteur sint occaecat cupidatat non "
        #                                "proident, sunt in culpa qui officia deserunt "
        #                                "mollit anim id est laborum.",
        #                           size_hint_y=None,
        #                           valign='top')
        #         content.bind(texture_size=content.setter('size'))
        #         self.dialog = MDDialog(title="This is a long test dialog",
        #                                content=content,
        #                                size_hint=(.8, None),
        #                                height=dp(200),
        #                                auto_dismiss=False)
        #
        #         self.dialog.add_action_button("Dismiss",
        #                                       action=lambda *x: self.dialog.dismiss())
        #         self.dialog.open()
        #         print("opened?")
        # with open("used.txt", "w") as file:
        #     file.write("1")
        self.search()

    def on_leave(self, *args):
        self.screenlist.append("MenuScreen")
        print("MenuScreen's list: ", self.screenlist)


class DateScreen(Screen):
    date = StringProperty('')
    otherdate = StringProperty('')
    screenlist = ListProperty([])
    count = 0

    def __init__(self, **kwargs):
        # screenlist = self.screenlist
        super(DateScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.screenlist.append("DateScreen")
        self.show_date_picker()

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj
        dt = datetime.strptime(str(date_obj), '%Y-%m-%d')
        # actualDate = '{0}-{1}-{2}'.format(dt.day, dt.strftime("%b"), dt.year % 100)
        actualDate = dt.strftime("%#d-%b-%y")
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
        self.manager.current = "DetailsScreen"


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
class DetailsScreen(Screen):
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasa = StringProperty('')
    tmaasa = StringProperty('')
    paksha = StringProperty('')
    thithi = StringProperty('')
    vara = StringProperty('')
    date = StringProperty('')
    nakshatra = StringProperty('')
    nakshatraTime = StringProperty('')
    nakshatra2 = StringProperty('')
    nakshatra2Time = StringProperty('')
    note1 = StringProperty('')
    note2 = StringProperty('')
    note3 = StringProperty('')
    note4 = StringProperty('')
    screenlist = ListProperty([])
    count = NumericProperty()

    def on_pre_enter(self, *args):
        self.count = 0
        self.screenlist.append("DateScreen")
        print(self.screenlist)
        success = self.search()
        if success == -1:
            self.count += 1
            self.manager.current = "DateScreen"

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
TM.TeluguMaasa,
V.Vaaram,
T.Thithi,
N.Nakshatra,
C.Nakshtra1Time,
C.Nakshtra2Time,
C.Notes1,
C.Notes2,
C.Notes3,
C.Notes4
FROM Calendar2018 C, Samvatsaram S, Ayanam A, Rithu R, TamilMaasa M, TeluguMaasa TM, Vaaram V, Thithi T, Nakshatra N
WHERE date = ? AND S.ID =
                        C.samvatsaram AND A.ID = C.ayanam AND R.ID = C.rithu AND M.ID = C.TamilMaasa AND TM.ID = C.TeluguMaasa AND
  V.ID = C.vaaram AND T.ID = C.Thithi1 AND N.ID = C.Nakshtra1 ''',
            (date,))
        thing = cur.fetchone()
        print(thing)
        if thing is None:
            return -1
        else:
            self.samva = thing[1] + " nama samvatsarae"
            self.avanam = thing[2]
            self.rithu = thing[3] + "a rithu"
            self.maasa = "Tamil Maasa: " + thing[4] + " maasae"
            self.tmaasa = "Telugu Maasa: " + thing[5] + " maasae"
            self.paksha = "heehee" + " paksha"
            self.vara = thing[6]
            self.thithi = thing[7] + " thithu"
            self.nakshatraTime = thing[9]
            self.nakshatra = thing[8] + " nakshatra starts at " + self.nakshatraTime
            self.nakshatra2Time = thing[11]
            self.nakshatra2 = thing[10] + " nakshatra starts at " + self.nakshatra2Time


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


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
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
