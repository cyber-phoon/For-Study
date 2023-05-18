import os
import cv2
import dlib
import tempfile
import mysql.connector
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import codecs

class Add_Persons_Window():
    def __init__(self):
        self.root = Tk()
        bold_font = ("Tahoma", 10, "bold")
        self.root.configure(bg="light blue")
        self.root.geometry("325x158")
        self.root.title('Форма добавления данных')

        # Создание меток и полей для ввода данных
        Label(self.root, text='Имя:', font=bold_font, bg="#87cefa", fg="black").grid(row=0, column=0, sticky=W)
        self.first_name_entry = Entry(self.root)
        self.first_name_entry.grid(row=0, column=1)

        Label(self.root, text='Фамилия:', font=bold_font, bg="#87cefa", fg="black").grid(row=1, column=0, sticky=W)
        self.last_name_entry = Entry(self.root)
        self.last_name_entry.grid(row=1, column=1)

        Label(self.root, text='Отчество:', font=bold_font, bg="#87cefa", fg="black").grid(row=2, column=0, sticky=W)
        self.patronymic_entry = Entry(self.root)
        self.patronymic_entry.grid(row=2, column=1)

        # Создание метки и кнопки для выбора файла с фотографией
        Label(self.root, text='Фотография:', font=bold_font, bg="#87cefa", fg="black").grid(row=3, column=0, sticky=W)
        self.face_photo_path = StringVar()
        self.face_photo_entry = Entry(self.root, textvariable=self.face_photo_path, state='readonly')
        self.face_photo_entry.grid(row=3, column=1)

        self.face_photo_button = Button(self.root, text='Сделать фото', command=self.face_photo_button_clicked, font=bold_font, bg="#87cefa", fg="black")
        self.face_photo_button.grid(row=3, column=2)
        self.face_photo_button.bind("<Enter>", self.on_enter)
        self.face_photo_button.bind("<Leave>", self.on_leave)

        # Создание кнопки "Добавить"
        self.add_button = Button(self.root, text='Добавить', command=self.add_button_clicked, font=bold_font, bg="#87cefa", fg="black")
        self.add_button.grid(row=4, column=1)
        self.add_button.bind("<Enter>", self.on_enter)
        self.add_button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget.config(bg="white", fg="#87cefa")

    def on_leave(self, event):
        event.widget.config(bg="#87cefa", fg="black")

    def face_photo_button_clicked(self):
        # Захват изображения с камеры
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # Создание временного файла изображения
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            file_path = f.name
            cv2.imwrite(file_path, frame)
            self.face_photo_path.set(file_path)

        # Отображение изображения в новом окне
        image = cv2.imread(file_path)
        detector = dlib.get_frontal_face_detector()
        image = cv2.imread(file_path)
        faces = detector(image, 1)
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        window_title = "Photo".encode('utf-8')
        cv2.imshow(codecs.decode(window_title, 'utf-8'), image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Создание кнопки "Добавить"
    def add_button_clicked(self):
        if self.first_name_entry.get() and self.last_name_entry.get() and self.patronymic_entry.get() and self.face_photo_path.get():
            try:
                connection = mysql.connector.connect(user='root', password='qw123', database='diploma')
                cursor = connection.cursor()
                query = "INSERT INTO People (first_name, last_name, patronymic, face_photo) VALUES (%s, %s, %s, %s)"
                values = (self.first_name_entry.get(), self.last_name_entry.get(), self.patronymic_entry.get(), open(self.face_photo_path.get(), 'rb').read())
                cursor.execute(query, values)
                connection.commit()
                cursor.close()
                connection.close()
                self.first_name_entry.delete(0, END)
                self.last_name_entry.delete(0, END)
                self.patronymic_entry.delete(0, END)
                self.face_photo_path.set('')
                messagebox.showinfo("Успех", "Данные успешно добавлены в базу данных.")
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка")
        else:
            messagebox.showerror("Ошибка добавления данных", "Пожалуйста, заполните все поля.")

    def run(self):
        self.root.mainloop()