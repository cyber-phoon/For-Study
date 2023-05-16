import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import mysql.connector
#from showallpeople import ShowAllBd

class RequestGU():
    def __init__(self):
        self.action_combobox = None
        # создаем соединение с базой данных и курсор
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )
        self.cursor = self.conn.cursor()

        # список допустимых значений для запроса и действия
        self.valid_requests = ["Запрос на изменение параметров пользователя", "Запрос на устранение неполадок"]
        self.valid_actions = {
            "Запрос на изменение параметров пользователя": ["Изменение ФИО", "Обновление фотографии", "Удаление пользователя"],
            "Запрос на устранение неполадок": ["Неполадки с видеооборудованием", "Неполадки с турникетом"]
        }


        # создаем окно tkinter
        self.root = tk.Tk()
        self.root.geometry('1500x500')
        self.root.title("Добавление запроса")

        # создаем метки и выпадающие списки для запроса и действия
        request_label = tk.Label(self.root, text="Запрос:")
        request_label.pack()
        self.request_var = tk.StringVar()
        self.request_combobox = ttk.Combobox(self.root, textvariable=self.request_var, values=self.valid_requests, state="readonly", width=40)
        self.request_combobox.pack()
        self.request_combobox.bind("<<ComboboxSelected>>", self.update_actions)

        action_label = tk.Label(self.root, text="Действие:")
        action_label.pack()
        self.action_var = tk.StringVar()
        self.action_combobox = ttk.Combobox(self.root, textvariable=self.action_var, values=[], state="readonly", width=30)
        self.action_combobox.pack()
        self.action_combobox.bind("<<ComboboxSelected>>", self.update_fio)

        comment_label = tk.Label(self.root, text="Комментарий:")
        comment_label.pack()
        self.comment_entry = tk.Entry(self.root, width=20)
        self.comment_entry.pack()

        self.fio_label = tk.Label(self.root, text="ФИО:")
        self.entry_fio_label = tk.Entry(self.root)
        self.fio_label.pack()
        self.entry_fio_label.pack()
        self.entry_fio_label.pack_forget()
        self.fio_label.pack_forget()

        # создаем кнопку для добавления запроса
        self.add_button = tk.Button(self.root, text="Добавить", command=self.add_request)
        self.add_button.pack()

        # создаем кнопку для отображения людей
        self.show_button = tk.Button(self.root, text="Показать людей", command=self.show_all_people)

        # скрываем кнопку по умолчанию
        self.show_button.pack()
        self.show_button.pack_forget()

        # создаем виджет Treeview
        self.treeview = ttk.Treeview(self.root, columns=("request", "action", "fio", "comment", "acceptance_status", "completion_status"))

        # добавляем заголовки столбцов
        self.treeview.heading("request", text="Запрос")
        self.treeview.heading("action", text="Действие")
        self.treeview.heading("fio", text="ФИО")
        self.treeview.heading("comment", text="Комментарий")
        self.treeview.heading("acceptance_status", text="Статус согласования")
        self.treeview.heading("completion_status", text="Статус выполнения")

        # выполняем запрос к базе данных и добавляем данные в Treeview
        self.cursor.execute("SELECT request, action, fio, comment, acceptance_status, completion_status FROM requests")
        rows = self.cursor.fetchall()
        for row in rows:
            item = list(row)
            if item[4] == None: item[4] = 'Передано на рассмотрение'
            if item[5] == None: item[5] = 'Передано на рассмотрение'
            row = tuple(item)
            self.treeview.insert("", tk.END, values=row)

        # отображаем Treeview в окне
        self.treeview.pack()

        # запускаем главный цикл окна tkinter
        self.root.mainloop()

        # закрываем соединение с базой данных при выходе из программы
        self.conn.close()



        # функция для обновления списка действий

    def update_actions(self, event=None):
        selected_request = self.request_combobox.get()
        if self.action_combobox is not None:
            if selected_request in self.valid_actions:
                self.action_combobox.config(values=self.valid_actions[selected_request])
                self.action_combobox.set('')
                self.show_button.pack_forget()
                self.fio_label.pack_forget()
                self.entry_fio_label.pack_forget()
            else:
                self.action_combobox.config(values=[])
                self.show_button.pack_forget()
                self.fio_label.pack_forget()
                self.entry_fio_label.pack_forget()

    def update_fio(self, event=None):
        selected_action = self.action_combobox.get()
        if selected_action in ("Изменение ФИО", "Удаление пользователя", "Обновление фотографии"):
            self.entry_fio_label.pack(side=BOTTOM)
            self.fio_label.pack(side=BOTTOM)
            self.show_button.pack()
        else:
            self.show_button.pack_forget()
            self.fio_label.pack_forget()
            self.entry_fio_label.pack_forget()

    # функция для добавления запроса в базу данных
    def add_request(self):
        # создаем соединение с базой данных и курсор
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )
        self.cursor = self.conn.cursor()
        # проверяем, что поля запроса и действия не пустые
        request = self.request_combobox.get()
        action = self.action_combobox.get()
        comment = self.comment_entry.get()
        fio = self.entry_fio_label.get()
        if request and action:
            # добавляем запрос в базу данных
            self.cursor.execute("INSERT INTO requests (request, action, fio, comment) VALUES (%s, %s, %s, %s)",
                            (request, action, fio, comment))
            self.conn.commit()
            tk.messagebox.showinfo("Успех", "Запрос успешно добавлен в базу данных!")
            self.people_window.destroy()
            self.show_button.pack_forget()
            self.fio_label.pack_forget()
            self.entry_fio_label.pack_forget()
            # очищаем поля ввода
            self.request_combobox.set('')
            self.action_combobox.set('')
            self.comment_entry.delete(0, tk.END)

            # очищаем таблицу и обновляем её
            self.treeview.delete(*self.treeview.get_children())
            self.cursor.execute("SELECT request, action, fio, comment, acceptance_status, completion_status FROM requests")
            rows = self.cursor.fetchall()
            for row in rows:
                item = list(row)
                if item[4] == None: item[4] = 'Передано на рассмотрение'
                if item[5] == None: item[5] = 'Передано на рассмотрение'
                row = tuple(item)
                self.treeview.insert("", tk.END, values=row)
        else:
            tk.messagebox.showerror("Ошибка", "Поля запроса и действия не могут быть пустыми.")

    def show_all_people(self):
        self.people_window = tk.Toplevel()
        self.people_window.title("Пользователи")

        # создаем соединение с базой данных и курсор
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT first_name, last_name, patronymic, time FROM people")
        data = self.cursor.fetchall()

        # Создаем заголовки таблицы
        headers = ["Имя", "Фамилия", "Отчество", "Дата и время"]

        # Создаем таблицу и выводим данные
        for i in range(len(headers)):
            self.root.grid_columnconfigure(i, weight=1)

        row = 0

        # Выводим заголовки в первую строку таблицы
        for col, header in enumerate(headers):
            label = tk.Label(self.people_window, text=header, font=("Times New Roman", 12, "bold"), relief=tk.RIDGE, padx=5,
                             pady=5)
            label.grid(row=row, column=col, sticky="ew")
        row += 1

        for i, record in enumerate(data):
            for j, value in enumerate(record):
                label = tk.Label(self.people_window, text=value, relief=tk.RIDGE, padx=5, pady=5)
                label.grid(row=row, column=j, sticky="ew")
                label.bind("<Double-Button-1>",
                           lambda event, row=i, values=record[:3], column=j: self.populate_fio_entry(row, values,
                                                                                                     column))
            row += 1

        # Задаем размеры окна и выводим его посередине сверху
        self.people_window.geometry("500x500")
        self.people_window.update_idletasks()
        width = self.people_window.winfo_width()
        height = self.people_window.winfo_height()
        x = (self.people_window.winfo_screenwidth() // 2) - (width // 2)
        y = 50
        self.people_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Закрываем соединение с базой данных
        self.conn.close()

    def populate_fio_entry(self, row, values, column):
        fio = " ".join(values)
        self.entry_fio_label.delete(0, tk.END)
        self.entry_fio_label.insert(0, fio)