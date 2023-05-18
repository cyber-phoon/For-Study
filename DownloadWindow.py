from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl
import os


class Download_Window():
    def __init__(self):
        self.root = Tk()
        bold_font = ("Tahoma", 10, "bold")
        self.root.configure(bg="light blue")
        self.root.title("Данные работника")
        self.root.geometry('319x120')
        self.root.resizable(False, False)

        Label(self.root, text='Имя:', font=bold_font, bg="#87cefa", fg="black").grid(row=0, column=0, sticky=W)
        self.first_name = Entry(self.root)
        self.first_name.grid(row=0, column=1)
        self.first_name.config(width=18)

        Label(self.root, text='Фамилия:', font=bold_font, bg="#87cefa", fg="black").grid(row=1, column=0, sticky=W)
        self.last_name = Entry(self.root)
        self.last_name.grid(row=1, column=1)
        self.last_name.config(width=18)

        Label(self.root, text='Отчество:', font=bold_font, bg="#87cefa", fg="black").grid(row=2, column=0, sticky=W)
        self.patronymic = Entry(self.root)
        self.patronymic.grid(row=2, column=1)
        self.patronymic.config(width=18)

        self.add_button = Button(self.root, text='Скачать', command=self.download_button_clicked, font=bold_font, bg="#87cefa", fg="black")
        self.add_button.grid(row=3, column=1)
        self.add_button.bind("<Enter>", self.on_enter)
        self.add_button.bind("<Leave>", self.on_leave)
        self.download_all = Button(self.root, text='Скачать все', command=self.are_you_sure, font=bold_font, bg="#87cefa", fg="black")
        self.download_all.grid(row=3, column=2)
        self.download_all.bind("<Enter>", self.on_enter)
        self.download_all.bind("<Leave>", self.on_leave)

        # Подключаемся к базе данных MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )
        self.cursor = self.conn.cursor()

    def on_enter(self, event):
        event.widget.config(bg="white", fg="#87cefa")

    def on_leave(self, event):
        event.widget.config(bg="#87cefa", fg="black")

    def download_button_clicked(self):
        # Получаем данные из полей ввода
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        patronymic = self.patronymic.get()

        # Проверяем, что все поля заполнены
        if not all((first_name, last_name, patronymic)):
            messagebox.showerror('Ошибка', 'Пожалуйста, заполните все поля')
            return

        # Формируем SQL-запрос на поиск данных в таблице recognition_log
        sql_query = f"SELECT * FROM recognition_log WHERE first_name='{first_name}' AND last_name='{last_name}' AND patronymic='{patronymic}'"

        # Получаем результаты запроса и записываем их в DataFrame
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()
        df = pd.DataFrame(results, columns=['id', 'first_name', 'last_name', 'patronymic', 'time_entry', 'time_exit',
                                            'time_spent'])

        if df.empty:
            messagebox.showwarning('Нет данных', 'Не найдено записей, соответствующих введенным данным')
            return

        # Создаем объект Workbook и добавляем в него лист
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Записываем данные из DataFrame в ячейки листа
        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)

        # Задаем имя файла и сохраняем его
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        filename = os.path.join(downloads_folder, f"{first_name}_{last_name}_{patronymic}.xlsx")
        workbook.save(filename)

        messagebox.showinfo('Файл создан', f'Файл {filename} успешно создан')
        self.root.destroy()

        # Коммитим изменения в базе данных
        self.conn.commit()

    def are_you_sure(self):
        result = messagebox.askyesno("Подтверждение", "Вы уверены?")
        if result:
            # prompt user to enter year and month
            time_input = simpledialog.askstring("Выберите промежуток времени",
                                                "Введите год и месяц (в формате 'гггг-мм'):")

            if time_input is None:
                return

            # convert time input to datetime object
            try:
                start_time = datetime.strptime(time_input, '%Y-%m')
            except ValueError:
                messagebox.showerror(message="Неправильный формат ввода времени.")
                return

            # get first and last days of the month
            start_time_str = start_time.strftime('%Y-%m-01 00:00:00')
            end_time_str = start_time.replace(day=1, month=start_time.month + 1, year=start_time.year).strftime(
                '%Y-%m-01 00:00:00')

            # query the database for the selected time range
            query = f"SELECT first_name, last_name, patronymic, time_entry, time_exit FROM recognition_log WHERE time_entry >= '{start_time_str}' AND time_exit < '{end_time_str}'"
            df = pd.read_sql_query(query, self.conn)

            if df.empty:
                messagebox.showerror(message="Нет данных за выбранный промежуток времени.")
                return

            # рассчет длительности в секундах
            df['time_spent'] = (df['time_exit'] - df['time_entry']).dt.total_seconds()

            # удаление строк, в которых есть пропущенные значения
            df.dropna(inplace=True)

            # преобразование длительности в строковый формат hh:mm:ss
            df['time_spent'] = df['time_spent'].apply(lambda x: str(timedelta(seconds=x)))

            # сохранение таблицы в файл Excel с добавлением даты и времени в название файла
            downloads_folder = os.path.join(os.environ['userprofile'], 'Downloads')
            current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(downloads_folder,
                                    f'recognition_log_{start_time.strftime("%Y%m")}_{current_datetime}.xlsx')
            df.to_excel(filename, index=False)

            messagebox.showinfo(message=f'Данные успешно скачаны в {downloads_folder}')

    def run(self):
        self.root.mainloop()


#download_window = Download_Window()
#download_window.run()
