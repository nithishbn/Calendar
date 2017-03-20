import sqlite3
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from plyer import vibrator

class LoginScreen(Screen):
    pass
class MenuScreen(Screen):
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasae = StringProperty('')
    pakshae = StringProperty('')
    thithi = StringProperty('')
    def today(self):
        # vibrator.vibrate(0.10)
        self.search()
        self.manager.current = 'TodayScreen'

    def search(self):
        date = "1/1/2017"
        conn = sqlite3.connect('calendar.sqlite')
        cur = conn.cursor()
        cur.execute(
            '''SELECT date, S.Name, A.Name, R.Name, M.Name, P.Name, V.Name, T.Name FROM Main JOIN Samvatsaram S on Main.samvatsaram = S.SID JOIN Ayanam A on Main.ayanam = A.AID JOIN Rithu R on Main.rithu = R.RID JOIN Maasae M on Main.maasa = M.MID JOIN Pakshae P on Main.pakshae = P.PID JOIN Vaaram V on Main.Vaaram = V.VID JOIN Thithi T on Main.thithi = T.TID WHERE date = ?''',
            (date,))
        thing = cur.fetchone()
        for query in thing:
            if query == thing[0]:
                print("Date:", query)
            elif query == thing[1]:
                print("Samvatsaramam:", query)
                self.samva = query
            elif query == thing[2]:
                print("Ayanam:", query)
                self.avanam = query
            elif query == thing[3]:
                print("Rithu:", query)
                self.rithu = query
            elif query == thing[4]:
                print("Maasae:", query)
                self.maasae = query
            elif query == thing[5]:
                print("Pakshae:", query)
                self.pakshae = query
            elif query == thing[6]:
                print("Day:", query)
            elif query == thing[7]:
                print("Thithi:", query)
                self.thithi = query


class TodayScreen(Screen):
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasae = StringProperty('')
    pakshae = StringProperty('')
    thithi = StringProperty('')

class InterfaceApp(App):
    pass


InterfaceApp().run()
