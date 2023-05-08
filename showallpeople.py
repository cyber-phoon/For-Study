import mysql.connector as mysql
import tkinter as tk

class ShowAllBd():
    def __init__(self):
        # Создаем окно
        self.root = tk.Toplevel()
        self.root.title("Данные из таблицы people")

        # Подключаемся к базе данных
        db = mysql.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )

        # Получаем данные из таблицы people
        cursor = db.cursor()
        cursor.execute("SELECT first_name, last_name, patronymic, time FROM people")
        data = cursor.fetchall()

        # Создаем заголовки таблицы
        headers = ["Имя", "Фамилия", "Отчество", "Дата и время"]

        # Создаем таблицу и выводим данные
        for i in range(len(headers)):
            self.root.grid_columnconfigure(i, weight=1)

        row = 0

        # Выводим заголовки в первую строку таблицы
        for col, header in enumerate(headers):
            label = tk.Label(self.root, text=header, font=("Helvetica", 10, "bold"), relief=tk.RIDGE, padx=5, pady=5)
            label.grid(row=row, column=col, sticky="ew")
        row += 1

        # Выводим данные в таблицу
        for record in data:
            for col, value in enumerate(record):
                label = tk.Label(self.root, text=value, relief=tk.RIDGE, padx=5, pady=5)
                label.grid(row=row, column=col, sticky="ew")
            row += 1

        # Задаем размеры окна и выводим его посередине сверху
        self.root.geometry("500x500")
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = 50
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Закрываем соединение с базой данных
        db.close()
