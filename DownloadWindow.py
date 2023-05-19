import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
import mysql.connector
import pandas as pd
import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def create_download_window(parent):
    download_frame = ttk.Frame(parent, padding='10')
    download_frame.pack()
    download_frame.configure(style="My.TFrame")


    bold_font = ("Tahoma", 10, "bold")

    first_name_label = tk.Label(download_frame, text='Имя:', font=bold_font, bg="#87cefa", fg="black")
    first_name_label.grid(row=0, column=0, sticky=tk.W)
    first_name = tk.Entry(download_frame)
    first_name.grid(row=0, column=1)
    first_name.config(width=18)

    last_name_label = tk.Label(download_frame, text='Фамилия:', font=bold_font, bg="#87cefa", fg="black")
    last_name_label.grid(row=1, column=0, sticky=tk.W)
    last_name = tk.Entry(download_frame)
    last_name.grid(row=1, column=1)
    last_name.config(width=18)

    patronymic_label = tk.Label(download_frame, text='Отчество:', font=bold_font, bg="#87cefa", fg="black")
    patronymic_label.grid(row=2, column=0, sticky=tk.W)
    patronymic = tk.Entry(download_frame)
    patronymic.grid(row=2, column=1)
    patronymic.config(width=18)

    add_button = tk.Button(download_frame, text='Скачать', command=lambda: download_button_clicked(first_name.get(), last_name.get(), patronymic.get()),
                           font=bold_font, bg="#87cefa", fg="black")
    add_button.grid(row=3, column=1)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

    download_all = tk.Button(download_frame, text='Скачать все', command=are_you_sure,
                             font=bold_font, bg="#87cefa", fg="black")
    download_all.grid(row=3, column=2)
    download_all.bind("<Enter>", on_enter)
    download_all.bind("<Leave>", on_leave)

    return download_frame

def on_enter(event):
    event.widget.config(bg="white", fg="#87cefa")

def on_leave(event):
    event.widget.config(bg="#87cefa", fg="black")

def download_button_clicked(first_name, last_name, patronymic):
    # Подключаемся к базе данных MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="qw123",
        database="diploma"
    )
    cursor = conn.cursor()

    # Проверяем, что все поля заполнены
    if not all((first_name, last_name, patronymic)):
        messagebox.showerror('Ошибка', 'Пожалуйста, заполните все поля')
        return

    # Формируем SQL-запрос на поиск данных в таблице recognition_log
    sql_query = f"SELECT * FROM recognition_log WHERE first_name='{first_name}' AND last_name='{last_name}' AND patronymic='{patronymic}'"

    # Получаем результаты запроса и записываем их в DataFrame
    cursor.execute(sql_query)
    results = cursor.fetchall()
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

    # Коммитим изменения в базе данных
    conn.commit()

def are_you_sure():
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
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )
        df = pd.read_sql_query(query, conn)

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
