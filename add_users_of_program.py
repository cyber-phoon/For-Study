import mysql.connector
from tkinter import ttk
from tkinter import messagebox
import hashlib


def create_users_program_widgets(parent):
    bold_font = ("Tahoma", 10, "bold")
    frame = ttk.Frame(parent, padding="10")
    frame.configure(style="My.TFrame")

    # Создание меток и полей для ввода данных
    ttk.Label(frame, text='Логин:', font=bold_font, background="#87cefa", borderwidth=2).grid(row=0, column=0, sticky="w")
    username = ttk.Entry(frame, width=18)
    username.grid(row=0, column=1)

    ttk.Label(frame, text='Пароль:', font=bold_font, background="#87cefa", borderwidth=2).grid(row=1, column=0, sticky="w")
    password = ttk.Entry(frame, width=18, show="*")
    password.grid(row=1, column=1)

    ttk.Label(frame, text='Роль:', font=bold_font, background="#87cefa", borderwidth=2).grid(row=2, column=0, sticky="w")
    roles = ["admin", "user"]
    role = ttk.Combobox(frame, values=roles, state='readonly', width=15)
    role.grid(row=2, column=1)

    def add_button_clicked():
        if username.get() and password.get() and role.get():
            try:
                connection = mysql.connector.connect(user='root', password='qw123', database='diploma')
                cursor = connection.cursor()

                # Хэширование пароля
                hashed_password = hashlib.sha256(password.get().encode('utf-8')).hexdigest()

                query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                values = (username.get(), hashed_password, role.get())
                cursor.execute(query, values)
                connection.commit()
                cursor.close()
                connection.close()
                username.delete(0, 'end')
                password.delete(0, 'end')
                messagebox.showinfo("Успех", "Данные успешно добавлены в базу данных.")
            except Exception as e:
                messagebox.showinfo("Ошибка")
        else:
            messagebox.showerror("Ошибка добавления данных", "Пожалуйста, заполните все поля.")

    add_button = ttk.Button(frame, text='Добавить', command=add_button_clicked)
    add_button.grid(row=3, column=1)

    return frame