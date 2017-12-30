import sqlite3
from datetime import datetime
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, ListProperty, NumericProperty, partial
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.button import MDIconButton
from kivymd.card import MDCard, MDSeparator
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBodyTouch
from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar
from plyer import call
import os
from sys import platform


class Navigation(NavigationLayout):
    def __init__(self):
        super(Navigation, self).__init__()
        self.screenlist = []
        Window.bind(on_keyboard=App.get_running_app().onBackBtn)

    def onNextScreen(self, root, next_screen):
        self.screenlist.append(root)
        self.ids.sm.current = next_screen

    def onBackBtn(self):
        print("on back")
        if self.screenlist:
            print(self.screenlist)
            self.ids.sm.current = self.screenlist.pop()
            return True
        return False


class MenuScreen(Screen):
    if platform == "win32":
        date = datetime.today().strftime("%#d-%b-%y")
    else:
        date = datetime.today().strftime("%-d-%b-%y")

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.search)

    def search(self, *args):
        date = self.date

        if datetime.today().year == 2017:
            date = "10-Mar-18"
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
  C.Notes4,
  C."Rahu Kalam",
  C.Varjyam,
  C.Durmuhurtam
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
        if data is not None:
            samva = MDLabel(text=data[1] + " nama samvatsarae", pos_hint={'x': 0.05}, font_style="Subhead",
                            halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(samva)
            ayanam = MDLabel(text=data[2], pos_hint={'x': 0.05}, font_style="Subhead", halign="left",
                             theme_text_color="Primary")
            self.ids.labels.add_widget(ayanam)
            rithu = MDLabel(text=data[3] + " rithu", pos_hint={'x': 0.05}, font_style="Subhead", halign="left",
                            theme_text_color="Primary")
            self.ids.labels.add_widget(rithu)
            maasa = MDLabel(text="Tamil Maasa: " + data[4] + " maasae", pos_hint={'x': 0.05}, font_style="Subhead",
                            halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(maasa)
            tmaasa = MDLabel(text="Telugu Maasa: " + data[5] + " maasae", pos_hint={'x': 0.05}, font_style="Subhead",
                             halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(tmaasa)
            paksha = MDLabel(text=data[6] + " paaksha", pos_hint={'x': 0.05}, font_style="Subhead", halign="left",
                             theme_text_color="Primary")
            self.ids.labels.add_widget(paksha)
            thithi1Time = data[8]
            thithi1 = MDLabel(text=data[7] + " thithu starts at " + thithi1Time.strip(), pos_hint={'x': 0.05},
                              font_style="Subhead", halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(thithi1)

            if data[9] is not None:
                thithi2Time = data[10]
                if thithi2Time == "(whole day)":
                    thithi2 = MDLabel(text=data[9] + " thithu lasts the entire day", pos_hint={'x': 0.05},
                                      font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(thithi2)
                else:
                    thithi2 = MDLabel(text=data[9] + " thithu starts at " + thithi2Time.strip(), pos_hint={'x': 0.05},
                                      font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(thithi2)
            # elif isinstance(self.ids.thithi2, MDLabel):
            #     self.ids.labels.remove_widget(self.ids.thithi2)
            vara = MDLabel(text=data[11], pos_hint={'x': 0.05}, font_style="Subhead",
                           halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(vara)
            nakshatraTime = data[13]
            nakshatra = MDLabel(text=data[12] + " nakshatra starts at " + nakshatraTime.strip(), pos_hint={'x': 0.05},
                                font_style="Subhead",
                                halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(nakshatra)
            if data[20] is not "" and data[20] != "NULL":
                self.ids.labels.add_widget(MDLabel(text="Rahu Kalam: " + data[20], theme_text_color='Primary',
                                                   font_style='Subhead', pos_hint={'x': 0.05}))
            print(data[21])
            if data[21] is not "" and data[21] != "NULL":
                self.ids.labels.add_widget(MDLabel(text="Varjyam: " + data[21], theme_text_color='Primary',
                                                   font_style='Subhead', pos_hint={'x': 0.05}))
            if data[22] is not "" and data[22] != "NULL":
                self.ids.labels.add_widget(MDLabel(text="Durmhurtam: " + data[22], theme_text_color='Primary',
                                                   font_style='Subhead', pos_hint={'x': 0.05}))
            if data[14] is not None:
                nakshatra2Time = data[15]
                if self.nakshatra2Time == "Whole day":
                    nakshatra2 = MDLabel(text=data[14] + " nakshatra lasts the entire day", pos_hint={'x': 0.05},
                                         font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(nakshatra2)
                else:
                    nakshatra2 = MDLabel(text=data[14] + " nakshatra starts at " + self.nakshatra2Time.strip(),
                                         pos_hint={'x': 0.05},
                                         font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(nakshatra2)
            # elif isinstance(self.ids.nakshatra2, MDLabel):
            #     self.ids.labels.remove_widget(self.ids.nakshatra2)
            if data[16] is "" and data[17] is "" and data[18] is "" and data[19] is "":
                self.ids.notesList.add_widget(MDLabel(text="No special events today!",
                                                      font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
            else:
                if data[16] is not "":
                    self.ids.notesList.add_widget(MDLabel(text=data[16], theme_text_color='Primary',
                                                          font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
                if data[17] is not "":
                    self.ids.notesList.add_widget(MDLabel(text=data[17], theme_text_color='Primary',
                                                          font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
                if data[18] is not "":
                    print("rogerroger")
                    self.ids.notesList.add_widget(MDLabel(text=data[18], theme_text_color='Primary',
                                                          font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
                if data[19] is not "":
                    print("roger")
                    self.ids.notesList.add_widget(MDLabel(text=data[19], theme_text_color='Primary',
                                                          font_style='Subhead', pos_hint={'x': 0.05}))


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
        previous_date = date_obj
        print(previous_date)
        dt = datetime.strptime(str(date_obj), '%Y-%m-%d')
        if dt.year != 2018:
            pass
        else:
            if platform == "win32":
                actualDate = dt.strftime("%#d-%b-%y")
            else:
                actualDate = dt.strftime("%-d-%b-%y")
            self.date = str(actualDate)
            self.selectdate()

    def show_date_picker(self):
        MDDatePicker(self.set_previous_date).open()

    def selectdate(self):
        App.get_running_app().root.onNextScreen(self.manager.current, "DetailsScreen")


class DetailsScreen(Screen):
    date = StringProperty('')

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.search)
        # if success == -1:
        #     self.count -= 1
        #     print("leaving detailsscreen", self.count)
        #     self.manager.current = "DateScreen"

    def search(self, *args):
        date = self.date
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
  C.Notes4,
  C."Rahu Kalam",
  C.Varjyam,
  C.Durmuhurtam
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
            date1 = datetime.strptime(date, "%d-%b-%y")
            self.date = date1.strftime("%B %d") + " Events"
            
            samva = MDLabel(id="samva", text=data[1] + " nama samvatsarae", pos_hint={'x': 0.05}, font_style="Subhead",
                            halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(samva)
            print(self.ids.labels.ids)
            ayanam = MDLabel(id="ayanam", text=data[2], pos_hint={'x': 0.05}, font_style="Subhead", halign="left",
                             theme_text_color="Primary")
            self.ids.labels.add_widget(ayanam)
            rithu = MDLabel(id="rithu", text=data[3] + " rithu", pos_hint={'x': 0.05}, font_style="Subhead",
                            halign="left",
                            theme_text_color="Primary")
            self.ids.labels.add_widget(rithu)
            maasa = MDLabel(id="maasa", text="Tamil Maasa: " + data[4] + " maasae", pos_hint={'x': 0.05},
                            font_style="Subhead",
                            halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(maasa)
            tmaasa = MDLabel(id="tmaasa", text="Telugu Maasa: " + data[5] + " maasae", pos_hint={'x': 0.05},
                             font_style="Subhead",
                             halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(tmaasa)
            paksha = MDLabel(id="paksha", text=data[6] + " paaksha", pos_hint={'x': 0.05}, font_style="Subhead",
                             halign="left",
                             theme_text_color="Primary")
            self.ids.labels.add_widget(paksha)
            thithi1Time = data[8]
            thithi1 = MDLabel(id="thithi1", text=data[7] + " thithu starts at " + thithi1Time.strip(),
                              pos_hint={'x': 0.05},
                              font_style="Subhead", halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(thithi1)

            if data[9] is not None:
                thithi2Time = data[10]
                if thithi2Time == "(whole day)":
                    thithi2 = MDLabel(id="thithi2", text=data[9] + " thithu lasts the entire day", pos_hint={'x': 0.05},
                                      font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(thithi2)
                else:
                    thithi2 = MDLabel(id="thithi2", text=data[9] + " thithu starts at " + thithi2Time.strip(),
                                      pos_hint={'x': 0.05},
                                      font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(thithi2)
            vara = MDLabel(id="vara", text=data[11], pos_hint={'x': 0.05}, font_style="Subhead",
                           halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(vara)
            nakshatraTime = data[13]
            nakshatra = MDLabel(id="nakshatra", text=data[12] + " nakshatra starts at " + nakshatraTime.strip(),
                                pos_hint={'x': 0.05},
                                font_style="Subhead",
                                halign="left", theme_text_color="Primary")
            self.ids.labels.add_widget(nakshatra)
            if data[20] is not "" and data[20] != "NULL":
                self.ids.labels.add_widget(
                    MDLabel(id="rahu", text="Rahu Kalam: " + data[20], theme_text_color='Primary',
                            font_style='Subhead', pos_hint={'x': 0.05}))
            if data[21] is not "" and data[21] != "NULL":
                self.ids.labels.add_widget(
                    MDLabel(id="varjyam", text="Varjyam: " + data[21], theme_text_color='Primary',
                            font_style='Subhead', pos_hint={'x': 0.05}))
            if data[22] is not "" and data[22] != "NULL":
                self.ids.labels.add_widget(
                    MDLabel(id="durmu", text="Durmhurtam: " + data[22], theme_text_color='Primary',
                            font_style='Subhead', pos_hint={'x': 0.05}))
            if data[14] is not None:
                nakshatra2Time = data[15]
                if self.nakshatra2Time == "Whole day":
                    nakshatra2 = MDLabel(id="nakshatra2", text=data[14] + " nakshatra lasts the entire day",
                                         pos_hint={'x': 0.05},
                                         font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(nakshatra2)
                else:
                    nakshatra2 = MDLabel(id="nakshatra2",
                                         text=data[14] + " nakshatra starts at " + self.nakshatra2Time.strip(),
                                         pos_hint={'x': 0.05},
                                         font_style="Subhead", halign="left", theme_text_color="Primary")
                    self.ids.label.add_widget(nakshatra2)
            if data[16] is "" and data[17] is "" and data[18] is "" and data[19] is "":
                self.ids.notesList.add_widget(
                    MDLabel(id="note0", text="No special events today!", theme_text_color='Primary',
                            font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
            else:
                if data[16] is not "":
                    self.ids.notesList.add_widget(MDLabel(id="note1", text=data[16], theme_text_color='Primary',
                                                          font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
                if data[17] is not "":
                    self.ids.notesList.add_widget(MDLabel(id="note2", text=data[17], theme_text_color='Primary',
                                                          font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
                if data[18] is not "":
                    print("rogerroger")
                    self.ids.notesList.add_widget(MDLabel(id="note3", text=data[18], theme_text_color='Custom',
                                                          font_style='Subhead', pos_hint={'x': 0.05, 'top': 1}))
                if data[19] is not "":
                    print("roger")
                    self.ids.notesList.add_widget(MDLabel(id="note4", text=data[19], theme_text_color='Primary',
                                                          font_style='Subhead', pos_hint={'x': 0.05}))


class ConstructionScreen(Screen):
    pass


class GalleryScreen(Screen):
    imagefile = StringProperty("./images/2014-10-01-01.00.23.jpg")
    filenames = ListProperty([])
    count = NumericProperty(0)
    lengthoflist = NumericProperty()

    def on_enter(self, *args):
        print(self.manager)
        self.count = 0
        # self.filenames = []
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
        if platform != "win32":
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
    icon = "./icon.png"

    def build(self):
        # self.theme_cls.
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.accent_palette = "Blue"
        # self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_dark_hue = "A100"

    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc key """
        # 27 is back press number code
        if key == 27:
            print("hixd")
            # Call the "OnBackBtn" method from the "ExampleRoot" instance
            return self.root.onBackBtn()
        return False

    def on_pause(self):
        return True


if __name__ == '__main__':
    InterfaceApp().run()
