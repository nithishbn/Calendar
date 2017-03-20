import sqlite3
def newuser():
    print("Welcome!")
    print("Quickly sign up or login: ")
    inp = input()
    if inp == "sign up":
        name = input("First name: ")
        name2 = input("Middle name")

    elif inp == "login":
        user = input("Username: ")
        passw = input("Password: ")
