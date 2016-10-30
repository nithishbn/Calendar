import sqlite3

# for line in f:
#     search = re.findall("^([1-9])", line)
#     print(search)
conn = sqlite3.connect('calendar.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Main;
DROP TABLE IF EXISTS Samvatsaram;
DROP TABLE IF EXISTS Ayanam;
DROP TABLE IF EXISTS Rithu;
DROP TABLE IF EXISTS Maasae;
DROP TABLE IF EXISTS Pakshae;
DROP TABLE IF EXISTS Vaaram;
DROP TABLE IF EXISTS Thithi;
CREATE TABLE Main (keycode INTEGER, date TEXT, day INTEGER, main_event TEXT, samvatsaram INTEGER, ayanam INTEGER, rithu INTEGER, maasa INTEGER, pakshae INTEGER, vaaram INTEGER, thithi INTEGER);
CREATE TABLE Samvatsaram (SID INTEGER, Name TEXT);
CREATE TABLE Ayanam (AID INTEGER, Name TEXT);
CREATE TABLE Rithu (RID INTEGER, Name TEXT);
CREATE TABLE Maasae (MID INTEGER, Name TEXT);
CREATE TABLE Pakshae (PID INTEGER, Name TEXT);
CREATE TABLE Vaaram (VID INTEGER, Name TEXT);
CREATE TABLE Thithi (TID INTEGER, Name TEXT);
SELECT Keycode FROM asdfsadgsynweqjk; ghsrah
''')
cur.executescript('''

''')


