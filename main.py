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
    def __init__(self):
        super(Navigation, self).__init__()
        self.screenlist = []
        Window.bind(on_keyboard=App.get_running_app().onBackBtn)

    def onNextScreen(self, root, next_screen):
        # add screen we were just in
        print(root)
        self.screenlist.append(root)
        print("just appeneded", self.screenlist)
        self.ids.sm.current = next_screen

    def onBackBtn(self):
        print("on back")
        if self.screenlist:
            print(self.screenlist)
            self.ids.sm.current = self.screenlist.pop()
            return True
        return False


class MenuScreen(Screen):
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

    def search(self):
        date = datetime.today().strftime("%d-%b-%y")
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()

        cur.execute(
            '''SELECT
  C."﻿Date",
  S.Samvatsaram,
  A.Ayanam,
  R.Rithu,
  M.TamilMaasa,
  TM.TeluguMaasa,
  P.Paksha,
  T.Thithi,
  C."Thithi1 Time",
  T2.Thithi,
  C."Thithi2 Time",
  V.Vaaram,
  N.Nakshatra,
  C.Nakshtra1Time,
  N2.Nakshatra,
  C.Nakshtra2Time,
  C.Notes1,
  C.Notes2,
  C.Notes3,
  C.Notes4
FROM Calendar2018 C
  JOIN Samvatsaram S ON C.Samvatsaram = S.ID
  JOIN Ayanam A ON C.Ayanam = A.ID
  JOIN Rithu R ON C.Rutau = R.ID
  JOIN TamilMaasa M ON C.TamilMaasa = M.ID
  JOIN TeluguMaasa TM ON C.TeluguMaasa = TM.ID
  JOIN Paksha P ON C.Paksha = P.PID
  JOIN Thithi T ON C.Thithi1 = T.ID
  LEFT JOIN Thithi T2 ON C.Thithi2 = T2.ID
  JOIN Vaaram V ON C.Vaaram = V.ID
  JOIN Nakshatra N ON C.Nakshtra1 = N.ID
  LEFT JOIN Nakshatra N2 ON C.Nakshtra2 = N2.ID
WHERE "﻿Date" = ?

''',
            (date,))
        data = cur.fetchone()
        print(data)
        if data is None:
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
            self.samva = data[1] + " nama samvatsarae"
            self.avanam = data[2]
            self.rithu = data[3] + "a rithu"
            self.maasa = "Tamil Maasa: " + data[4] + " maasae"
            self.tmaasa = "Telugu Maasa: " + data[5] + " maasae"
            self.paksha = "heehee" + " paksha"
            self.vara = data[6]
            self.thithi = data[7] + " thithu"
            self.nakshatraTime = data[9]
            self.nakshatra = data[8] + " nakshatra starts at " + self.nakshatraTime
            self.nakshatra2Time = data[11]
            self.nakshatra2 = data[10] + " nakshatra starts at " + self.nakshatra2Time

    def on_enter(self, *args):
        with open("used.txt", "r") as file:
            used = file.read()

            if used == "0":
                content = MDLabel(font_style='Body1',
                                  theme_text_color='Secondary',
                                  text="Lorem ipsum dolor sit amet, consectetur "
                                       "adipiscing elit, sed do eiusmod tempor "
                                       "incididunt ut labore et dolore magna aliqua. "
                                       "Ut enim ad minim veniam, quis nostrud "
                                       "exercitation ullamco laboris nisi ut aliquip "
                                       "ex ea commodo consequat. Duis aute irure "
                                       "dolor in reprehenderit in voluptate velit "
                                       "esse cillum dolore eu fugiat nulla pariatur. "
                                       "Excepteur sint occaecat cupidatat non "
                                       "proident, sunt in culpa qui officia deserunt "
                                       "mollit anim id est laborum.",
                                  size_hint_y=None,
                                  valign='top')
                content.bind(texture_size=content.setter('size'))
                self.dialog = MDDialog(title="This is a long test dialog",
                                       content=content,
                                       size_hint=(.8, None),
                                       height=dp(200),
                                       auto_dismiss=False)

                self.dialog.add_action_button("Dismiss",
                                              action=lambda *x: self.dialog.dismiss())
                self.dialog.open()
                print("opened?")
        with open("used.txt", "w") as file:
            file.write("1")
        self.search()


class DateScreen(Screen):
    date = StringProperty('')
    otherdate = StringProperty('')
    screenlist = ListProperty([])
    count = NumericProperty(0)

    def __init__(self, **kwargs):
        # screenlist = self.screenlist
        super(DateScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        print(self.count)
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
        App.get_running_app().root.onNextScreen(self.manager.current, "DetailsScreen")


class DetailsScreen(Screen):
    samva = StringProperty('')
    ayanam = StringProperty('')
    rithu = StringProperty('')
    maasa = StringProperty('')
    tmaasa = StringProperty('')
    paksha = StringProperty('')
    thithi1 = StringProperty('')
    thithi2 = StringProperty()
    thithi1Time = StringProperty('')
    thithi2Time = StringProperty('')
    vara = StringProperty('')
    date = StringProperty('')
    nakshatra = StringProperty('')
    nakshatraTime = StringProperty('')
    nakshatra2 = StringProperty()
    nakshatra2Time = StringProperty('')
    note1 = StringProperty('')
    note2 = StringProperty('')
    note3 = StringProperty('')
    note4 = StringProperty('')
    screenlist = ListProperty([])

    def on_pre_enter(self, *args):
        self.screenlist.append("DateScreen")
        print(self.screenlist)
        print("on pre", self.count)
        success = self.search()
        if success == -1:
            self.count -= 1
            print("leaving detailsscreen", self.count)
            self.manager.current = "DateScreen"

    def search(self):
        date = self.date
        print("search date function data: ", date)
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()

        cur.execute(
            '''SELECT
  C."﻿Date",
  S.Samvatsaram,
  A.Ayanam,
  R.Rithu,
  M.TamilMaasa,
  TM.TeluguMaasa,
  P.Paksha,
  T.Thithi,
  C."Thithi1 Time",
  T2.Thithi,
  C."Thithi2 Time",
  V.Vaaram,
  N.Nakshatra,
  C.Nakshtra1Time,
  N2.Nakshatra,
  C.Nakshtra2Time,
  C.Notes1,
  C.Notes2,
  C.Notes3,
  C.Notes4
FROM Calendar2018 C
  JOIN Samvatsaram S ON C.Samvatsaram = S.ID
  JOIN Ayanam A ON C.Ayanam = A.ID
  JOIN Rithu R ON C.Rutau = R.ID
  JOIN TamilMaasa M ON C.TamilMaasa = M.ID
  JOIN TeluguMaasa TM ON C.TeluguMaasa = TM.ID
  JOIN Paksha P ON C.Paksha = P.PID
  JOIN Thithi T ON C.Thithi1 = T.ID
  LEFT JOIN Thithi T2 ON C.Thithi2 = T2.ID
  JOIN Vaaram V ON C.Vaaram = V.ID
  JOIN Nakshatra N ON C.Nakshtra1 = N.ID
  LEFT JOIN Nakshatra N2 ON C.Nakshtra2 = N2.ID
WHERE "﻿Date" = ?

''',
            (date,))
        data = cur.fetchone()
        print(data)
        if data is None:
            return -1
        else:
            self.samva = data[1] + " nama samvatsarae"
            self.ayanam = data[2]
            self.rithu = data[3] + "a rithu"
            self.maasa = "Tamil Maasa: " + data[4] + " maasae"
            self.tmaasa = "Telugu Maasa: " + data[5] + " maasae"
            self.paksha = data[6] + " paksha"
            self.thithi1Time = data[8]
            self.thithi1 = data[7] + " thithu starts at " + self.thithi1Time.strip()
            if data[9] is not None:
                self.thithi2Time = data[10]
                if self.thithi2Time == "(whole day)":
                    self.thithi2 = data[9] + " thithu lasts the entire day"
                else:
                    self.thithi2 = data[9] + " thithu starts at " + self.thithi2Time.strip()
            else:
                self.ids.labels.remove_widget(self.ids.thithi2)
            self.vara = data[11]
            self.nakshatraTime = data[13]
            self.nakshatra = data[12] + " nakshatra starts at " + self.nakshatraTime.strip()

            if data[14] is not None:
                self.nakshatra2Time = data[15]
                if self.nakshatra2Time == "Whole day":
                    self.nakshatra2 = data[14] + " nakshatra lasts the entire day"
                else:
                    self.nakshatra2 = data[14] + " nakshatra starts at " + self.nakshatra2Time.strip()
            else:
                self.ids.labels.remove_widget(self.ids.nakshatra2)



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

    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc key """
        # 27 is back press number code
        if key == 27:
            print("hixd")
            # Call the "OnBackBtn" method from the "ExampleRoot" instance
            return self.root.onBackBtn()
        return False

    # def onBackBtn(self, window, key, *args):
    #     if key == 27:
    #         print("onBackBtn function call", self.screenlist)
    #         if len(self.screenlist) != 0:
    #             print("escaping")
    #             self.manager.current = self.screenlist[len(self.screenlist) - 1]
    #             self.screenlist.pop(len(self.screenlist) - 1)
    #             return True
    #         else:
    #             return False
    def on_pause(self):
        return True


if __name__ == '__main__':
    InterfaceApp().run()
