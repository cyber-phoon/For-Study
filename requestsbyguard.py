import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from showallpeople import ShowAllBd

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
        self.root.title("Добавление запроса")

        # создаем метки и выпадающие списки для запроса и действия
        request_label = tk.Label(self.root, text="Запрос:")
        request_label.pack()
        self.request_var = tk.StringVar()
        self.request_combobox = ttk.Combobox(self.root, textvariable=self.request_var, values=self.valid_requests, state="readonly")
        self.request_combobox.pack()
        self.request_combobox.bind("<<ComboboxSelected>>", self.update_actions)

        action_label = tk.Label(self.root, text="Действие:")
        action_label.pack()
        self.action_var = tk.StringVar()
        self.action_combobox = ttk.Combobox(self.root, textvariable=self.action_var, values=[], state="readonly")
        self.action_combobox.pack()
        self.action_combobox.bind("<<ComboboxSelected>>", self.update_fio)

        comment_label = tk.Label(self.root, text="Комментарий:")
        comment_label.pack()
        self.comment_entry = tk.Entry(self.root)
        self.comment_entry.pack()

        # создаем кнопку для добавления запроса
        self.add_button = tk.Button(self.root, text="Добавить", command=self.add_request)
        self.add_button.pack()

        # создаем кнопку для отображения людей
        self.show_button = tk.Button(self.root, text="Показать людей", command=self.show_all_people)

        # скрываем кнопку по умолчанию
        self.show_button.pack()
        self.show_button.pack_forget()

        # создаем кнопку для отображения людей
        self.make_photo = tk.Button(self.root, text="Сделать фотографию")

        # скрываем кнопку по умолчанию
        self.make_photo.pack()
        self.make_photo.pack_forget()

        # создаем кнопку для отображения людей
        self.delete_user = tk.Button(self.root, text="Удаление пользователя")

        # скрываем кнопку по умолчанию
        self.delete_user.pack()
        self.delete_user.pack_forget()

        # создаем виджет Treeview
        self.treeview = ttk.Treeview(self.root, columns=("request", "action", "comment", "acceptance_status", "completion_status"))

        # добавляем заголовки столбцов
        self.treeview.heading("request", text="Запрос")
        self.treeview.heading("action", text="Действие")
        self.treeview.heading("comment", text="Комментарий")
        self.treeview.heading("acceptance_status", text="Статус согласования")
        self.treeview.heading("completion_status", text="Статус выполнения")

        # выполняем запрос к базе данных и добавляем данные в Treeview
        self.cursor.execute("SELECT request, action, comment, acceptance_status, completion_status FROM requests")
        rows = self.cursor.fetchall()
        for row in rows:
            item = list(row)
            if item[3] == None: item[3] = 'Передано на рассмотрение'
            if item[4] == None: item[4] = 'Передано на рассмотрение'
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
            else:
                self.action_combobox.config(values=[])
                self.show_button.pack_forget()

    def update_fio(self, event=None):
        selected_action = self.action_combobox.get()
        if selected_action == "Изменение ФИО":
            self.show_button.pack()
        else:
            self.show_button.pack_forget()
        if selected_action == "Обновление фотографии":
            self.make_photo.pack()
        else:
            self.make_photo.pack_forget()
        if selected_action == "Удаление пользователя":
            self.delete_user.pack()
        else:
            self.delete_user.pack_forget()

    # функция для добавления запроса в базу данных
    def add_request(self):
        # проверяем, что поля запроса и действия не пустые
        request = self.request_combobox.get()
        action = self.action_combobox.get()
        comment = self.comment_entry.get()
        if request and action:
            # добавляем запрос в базу данных
            self.cursor.execute("INSERT INTO requests (request, action, comment) VALUES (%s, %s, %s)",
                            (request, action, comment))
            self.conn.commit()
            tk.messagebox.showinfo("Успех", "Запрос успешно добавлен в базу данных!")
            # очищаем поля ввода
            self.request_combobox.set('')
            self.action_combobox.set('')
            self.comment_entry.delete(0, tk.END)

            # очищаем таблицу и обновляем её
            self.treeview.delete(*self.treeview.get_children())
            self.cursor.execute("SELECT request, action, comment, acceptance_status, completion_status FROM requests")
            rows = self.cursor.fetchall()
            for row in rows:
                item = list(row)
                if item[3] == None: item[3] = 'Передано на рассмотрение'
                if item[4] == None: item[4] = 'Передано на рассмотрение'
                row = tuple(item)
                self.treeview.insert("", tk.END, values=row)
        else:
            tk.messagebox.showerror("Ошибка", "Поля запроса и действия не могут быть пустыми.")

    def show_all_people(self):
        show_all_people = ShowAllBd()
        show_all_people.root.mainloop()
