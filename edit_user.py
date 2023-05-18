import mysql.connector
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import codecs
import cv2
import numpy as np
import dlib
import tempfile

class Edit_Windows():

    def __init__(self, fio):
        # создаем главное окно приложения
        self.root = tk.Tk()
        bold_font = ("Tahoma", 10, "bold")
        self.root.configure(bg="light blue")
        self.root.title("Проверка данных")
        self.root.geometry('270x100')
        self.root.resizable(False,False)

        # создаем поля для ввода ФИО
        tk.Label(self.root, text="Имя:", font=bold_font, bg="#87cefa", fg="black").grid(row=0, column=0)
        self.entry_first_name = tk.Entry(self.root)
        self.entry_first_name.grid(row=0, column=1)
        tk.Label(self.root, text="Фамилия:", font=bold_font, bg="#87cefa", fg="black").grid(row=1, column=0)
        self.entry_last_name = tk.Entry(self.root)
        self.entry_last_name.grid(row=1, column=1)
        tk.Label(self.root, text="Отчество:", font=bold_font, bg="#87cefa", fg="black").grid(row=2, column=0)
        self.entry_patronymic = tk.Entry(self.root)
        self.entry_patronymic.grid(row=2, column=1)
        self.detector = dlib.get_frontal_face_detector()

        # создаем кнопку для проверки введенных данных
        tk.Button(self.root, text="Проверить данные", command=self.check_data, font=bold_font, bg="#87cefa", fg="black").grid(row=3, column=0, columnspan=2)

        self.entry_first_name.insert(0, fio[0])
        self.entry_last_name.insert(0, fio[1])
        self.entry_patronymic.insert(0, fio[2])

        self.root.mainloop()

    # функция для открытия окна для редактирования данных
    def edit_window(self, data):
        # создаем новое окно
        self.edit_win = tk.Toplevel()
        self.edit_win.geometry('320x150')
        self.edit_win.title("Редактирование данных")
        bold_font = ("Tahoma", 10, "bold")
        self.edit_win.configure(bg="light blue")
        tk.Label(self.edit_win, text="Имя:", font=bold_font, bg="#87cefa", fg="black").grid(row=0, column=0, sticky='e')
        self.entry_new_first_name = tk.Entry(self.edit_win)
        self.entry_new_first_name.grid(row=0, column=1, sticky='w')

        tk.Label(self.edit_win, text="Фамилия:", font=bold_font, bg="#87cefa", fg="black").grid(row=1, column=0,
                                                                                                sticky='e')
        self.entry_new_last_name = tk.Entry(self.edit_win)
        self.entry_new_last_name.grid(row=1, column=1, sticky='w')

        tk.Label(self.edit_win, text="Отчество:", font=bold_font, bg="#87cefa", fg="black").grid(row=2, column=0,
                                                                                                 sticky='e')
        self.entry_new_patronymic = tk.Entry(self.edit_win)
        self.entry_new_patronymic.grid(row=2, column=1, sticky='w')

        tk.Button(self.edit_win, text="Сделать фотографию", command=self.process_camera_photo, font=bold_font,
                  bg="#87cefa", fg="black", width=23).grid(row=3, column=0, columnspan=2)
        tk.Button(self.edit_win, text="Изменить введенное ФИО",
                  command=lambda: self.change_data(self.entry_first_name.get(), self.entry_last_name.get(),
                                                   self.entry_patronymic.get(), self.entry_new_first_name.get(),
                                                   self.entry_new_last_name.get(), self.entry_new_patronymic.get()),
                  font=bold_font, bg="#87cefa", fg="black", width=23).grid(row=4, column=0, columnspan=2)

    # функция, которая обрабатывает фото с камеры
    def process_camera_photo(self):
        cap = cv2.VideoCapture(0)  # открываем камеру

        while True:
            ret, frame = cap.read()  # считываем кадр с камеры
            # обнаружение лица на кадре
            faces = self.detector(frame, 0)
            # отрисовка квадрата вокруг каждого обнаруженного лица
            for face in faces:
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow('frame', frame)  # выводим кадр на экран

            cv2.imshow('frame', frame)  # выводим кадр на экран

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # если пользователь нажал 'q', то выходим из цикла
                break
            elif key == ord('s'):  # если пользователь нажал 's', то сохраняем фото в бд
                _, photo = cv2.imencode('.jpg', frame)  # сохраняем фото в закодированном формате
                self.save_changes(
                                  entry_first_name=self.entry_first_name.get(),
                                  entry_last_name=self.entry_last_name.get(),
                                  entry_patronymic=self.entry_patronymic.get(),
                                  photo=np.array(
                                      photo).tobytes())  # сохраняем фото в базу данных и обновляем запись для пользователя с id=1  # сохраняем фото в базу данных и обновляем запись для пользователя с id=1

        cap.release()  # освобождаем ресурсы камеры
        cv2.destroyAllWindows()  # закрываем все окна OpenCV


    # функция для проверки введенных данных в БД
    def check_data(self):
        cnx = mysql.connector.connect(host="localhost", user="root", password="qw123", database="diploma")
        cursor = cnx.cursor()

        # создаем запрос для поиска в БД
        query = "SELECT * FROM people WHERE "
        if self.entry_first_name.get():
            query += f"first_name='{self.entry_first_name.get()}' AND "
            print(self.entry_first_name)
        if self.entry_last_name.get():
            query += f"last_name='{self.entry_last_name.get()}' AND "
        if self.entry_patronymic.get():
            query += f"patronymic='{self.entry_patronymic.get()}' AND "
        if not (self.entry_first_name.get() or self.entry_last_name.get() or self.entry_patronymic.get()):
            tk.messagebox.showerror("Ошибка", "Введите хотя бы одно поле")
            return
        query = query[:-5]

        cursor.execute(query)
        result = cursor.fetchone()
        cnx.close()
        #print(result)
        if result:
            self.edit_window(result)
        else:
            tk.messagebox.showerror("Ошибка", "Пользователь не найден")

    def save_changes(self, entry_first_name, entry_last_name, entry_patronymic, photo):
        #print(photo)
        cnx = mysql.connector.connect(host="localhost", user="root", password="qw123", database="diploma")
        cursor = cnx.cursor()
        query = "UPDATE people SET face_photo=%s WHERE (first_name=%s OR last_name=%s OR patronymic=%s)"
        data = (photo, entry_first_name, entry_last_name, entry_patronymic)
        cursor.execute(query, data)
        cnx.commit()
        cnx.close()
        # выводим сообщение об успешном сохранении изменений
        tk.messagebox.showinfo("Успех", "Данные успешно сохранены")

    def change_data(self, entry_first_name, entry_last_name, entry_patronymic, entry_new_first_name,
                    entry_new_last_name, entry_new_patronymic):
        cnx = mysql.connector.connect(host="localhost", user="root", password="qw123", database="diploma")
        cursor = cnx.cursor()

        # ищем запись, которая соответствует одному из введенных Имени, Фамилии или Отчеству
        query_select = "SELECT first_name, last_name, patronymic FROM people WHERE first_name=%s OR last_name=%s OR patronymic=%s"
        data_select = (entry_first_name, entry_last_name, entry_patronymic)
        cursor.execute(query_select, data_select)
        result = cursor.fetchone()


        if result is None:
            # если запись не найдена, выводим сообщение об ошибке
            tk.messagebox.showerror("Ошибка", "Запись не найдена")
        else:
            # берем данные для изменения из найденной записи
            old_first_name, old_last_name, old_patronymic = result

            # обновляем данные
            new_first_name = self.entry_new_first_name.get() if self.entry_new_first_name.get() else old_first_name
            new_last_name = self.entry_new_last_name.get() if self.entry_new_last_name.get() else old_last_name
            new_patronymic = self.entry_new_patronymic.get() if self.entry_new_patronymic.get() else old_patronymic
            query_update = "UPDATE people SET first_name=%s, last_name=%s, patronymic=%s WHERE first_name=%s AND last_name=%s AND patronymic=%s"
            data_update = (new_first_name, new_last_name, new_patronymic, old_first_name, old_last_name, old_patronymic)
            cursor.execute(query_update, data_update)
            cnx.commit()
            cnx.close()
            # выводим сообщение об успешном сохранении изменений
            tk.messagebox.showinfo("Успех", "Данные успешно сохранены")



    #def editwindow(self):
        #editwindow = Edit_Windows()
        #editwindow.run()


