import sqlite3

# for line in f:
#     search = re.findall("^([1-9])", line)
#     print(search)
conn = sqlite3.connect('calendar.sqlite')
cur = conn.cursor()
print("Enter month/day/year (1/1/2017)")
date = input("Date: ")
def search():
    cur.execute('''SELECT date, S.Name, A.Name, R.Name, M.Name, P.Name, V.Name, T.Name FROM Main JOIN Samvatsaram S on Main.samvatsaram = S.SID JOIN Ayanam A on Main.ayanam = A.AID JOIN Rithu R on Main.rithu = R.RID JOIN Maasae M on Main.maasa = M.MID JOIN Pakshae P on Main.pakshae = P.PID JOIN Vaaram V on Main.Vaaram = V.VID JOIN Thithi T on Main.thithi = T.TID WHERE date = ?''', (date, ))
    thing = cur.fetchone()
    for query in thing:
        if query == thing[0]:
            print("Date:", query)
        elif query == thing[1]:
            print("Samvatsaramam:", query)
        elif query == thing[2]:
            print("Ayanam:", query)
        elif query == thing[3]:
            print("Rithu:", query)
        elif query == thing[4]:
            print("Maasae:", query)
        elif query == thing[5]:
            print("Pakshae:", query)
        elif query == thing[6]:
            print("Day:", query)
        elif query == thing[7]:
            print("Thithi:", query)

def main():
    search()
main()

#
# "SELECT date, S.Name, A.Name, R.Name, M.Name, P.Name, V.Name, T.Name FROM Main JOIN Samvatsaram S on Main.samvatsaram = S.SID JOIN Ayanam A on Main.ayanam = A.AID JOIN Rithu R on Main.rithu = R.RID JOIN Maasae M on Main.maasa = M.MID JOIN Pakshae P on Main.pakshae = P.PID JOIN Vaaram V on Main.Vaaram = V.VID JOIN Thithi T on Main.thithi = T.TID WHERE date = ?", (date, )