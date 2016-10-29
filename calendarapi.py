# import calendar
#
# cal = calendar.Calendar()
# print(cal.monthdayscalendar(2016, 2))
# print(calendar.isleap(2016))
# print(calendar.day_name())
import _sqlite3
conn = _sqlite3.connect('calendar.sqlite')
cur = conn.cursor()


