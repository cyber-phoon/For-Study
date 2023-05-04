from tkinter import *
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
import hashlib


class Users_Of_Program_Window():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("319x120")
        self.root.resizable(False, False)
        self.root.title('Добавление пользователя')

        # Создание меток и полей для ввода данных
        Label(self.root, text='Логин:').grid(row=0, column=0, sticky=W)
        self.username = Entry(self.root)
        self.username.grid(row=0, column=1)
        self.username.config(width=18)

        Label(self.root, text='Пароль:').grid(row=1, column=0, sticky=W)
        self.password = Entry(self.root)
        self.password.grid(row=1, column=1)
        self.password.config(width=18, show="*")

        Label(self.root, text='Роль:').grid(row=2, column=0, sticky=W)
        roles = ["admin", "user"]
        self.role = ttk.Combobox(self.root, values=roles, state='readonly')
        self.role.grid(row=2, column=1)
        self.role.config(width=15)

        add_button = Button(self.root, text='Добавить', command=self.add_button_clcked)
        add_button.grid(row=3, column=1)

    def add_button_clcked(self):
        if self.username.get() and self.password.get() and self.role.get():
            try:
                connection = mysql.connector.connect(user='root', password='qw123', database='diploma')
                cursor = connection.cursor()

                # Хэширование пароля
                hashed_password = hashlib.sha256(self.password.get().encode('utf-8')).hexdigest()

                query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                values = (self.username.get(), hashed_password, self.role.get())
                cursor.execute(query, values)
                connection.commit()
                cursor.close()
                connection.close()
                self.username.delete(0, END)
                self.password.delete(0, END)
                messagebox.showinfo("Успех", "Данные успешно добавлены в базу данных.")
                self.root.destroy()
            except Exception as e:
                messagebox.showinfo("Ошибка")
        else:
            messagebox.showerror("Ошибка добавления данных", "Пожалуйста, заполните все поля.")

    def run(self):
        self.root.mainloop()


