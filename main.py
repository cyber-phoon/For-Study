from interfacelogin import LoginWindow #Выход к интерфейсу
from Database import DB #Доступ к БД
from WorkWithDB import DB_Work #Переходник для работы с БД
import tkinter as tk

db = DB()
conn, cursor = db.get_conn_and_cursor()
db_work = DB_Work(conn, cursor)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('240x150')
    root.resizable(width=False, height=False)
    login_window = LoginWindow(root, db_work)
    root.mainloop()