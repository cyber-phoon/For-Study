import tkinter as tk
from tkinter import ttk
from admininterface import AdminWindow
from guardinterface import GuardWindow
from tkinter import messagebox


class LoginWindow():
    def __init__(self, master, db_work):
        self.master = master
        self.master.title("Авторизация")
        self.db_work = db_work
        self.master.configure(bg="light blue")
        bold_font = ("Tahoma",10,"bold")

        # Изменение цвета фона и текста внутри кнопки на светло-голубой

        self.username_label = tk.Label(self.master, text="Логин:", borderwidth=2, font=bold_font, bg="#87cefa")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_label = tk.Label(self.master, text="Пароль:", borderwidth=2, font=bold_font, bg="#87cefa")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        # Создание кнопки
        self.login_button = tk.Button(self.master, text="Войти", command=self.login, font=("Tahoma", 10, "bold"),
                                      relief="flat", bg="#87cefa", fg="black")
        self.login_button.pack(pady=10)
        self.login_button.bind("<Enter>", self.on_enter)
        self.login_button.bind("<Leave>", self.on_leave)

        self.master.bind('<Return>', lambda event: self.login())

    def on_enter(self, event):
        self.login_button.config(bg="white")

    def on_leave(self, event):
        self.login_button.config(bg="#87cefa")

    def login(self):
        # Retrieve username and password entered by user
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if entered username and password match stored credentials
        result = self.db_work.show_profile_by_username_and_password(username, password)

        if result:
            role = result[3]
            if role == 'admin':
                self.master.destroy()
                root = tk.Tk()
                admin_interface = AdminWindow(root,self.db_work)
            if role == "user":
                self.master.destroy()
                root = tk.Tk()
                guard_interface = GuardWindow(root,self.db_work)
        else:
            # Failed login
            messagebox.showinfo(title='Ошибка', message='Некорректное имя пользователя или пароль')
            print('Invalid username or password.')