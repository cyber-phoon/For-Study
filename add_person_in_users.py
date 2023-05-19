import os
import cv2
import dlib
import tempfile
import mysql.connector
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import codecs

def create_add_persons_widgets(parent_frame):
    bold_font = ("Tahoma", 10, "bold")
    frame = ttk.Frame(parent_frame, padding="10")
    frame.configure(style="My.TFrame")
    frame.pack()

    # Создание меток и полей для ввода данных
    Label(frame, text='Имя:', font=bold_font, bg="#87cefa", fg="black").grid(row=0, column=0, sticky=W)
    first_name_entry = Entry(frame)
    first_name_entry.grid(row=0, column=1)

    Label(frame, text='Фамилия:', font=bold_font, bg="#87cefa", fg="black").grid(row=1, column=0, sticky=W)
    last_name_entry = Entry(frame)
    last_name_entry.grid(row=1, column=1)

    Label(frame, text='Отчество:', font=bold_font, bg="#87cefa", fg="black").grid(row=2, column=0, sticky=W)
    patronymic_entry = Entry(frame)
    patronymic_entry.grid(row=2, column=1)

    # Создание метки и кнопки для выбора файла с фотографией
    Label(frame, text='Фотография:', font=bold_font, bg="#87cefa", fg="black").grid(row=3, column=0, sticky=N)
    face_photo_path = StringVar()
    face_photo_entry = Entry(frame, textvariable=face_photo_path, state='readonly')
    face_photo_entry.grid(row=3, column=1, sticky=N)

    def face_photo_button_clicked():
        # Захват изображения с камеры
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # Создание временного файла изображения
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            file_path = f.name
            cv2.imwrite(file_path, frame)
            face_photo_path.set(file_path)

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

    def on_enter(event):
        event.widget.config(bg="white", fg="#87cefa")

    def on_leave(event):
        event.widget.config(bg="#87cefa", fg="black")

    face_photo_button = Button(frame, text='Сделать фото', command=face_photo_button_clicked, font=bold_font, bg="#87cefa", fg="black")
    face_photo_button.grid(row=3, column=2)
    face_photo_button.bind("<Enter>", on_enter)
    face_photo_button.bind("<Leave>", on_leave)

    def add_button_clicked():
        if first_name_entry.get() and last_name_entry.get() and patronymic_entry.get() and face_photo_path.get():
            try:
                connection = mysql.connector.connect(user='root', password='qw123', database='diploma')
                cursor = connection.cursor()
                query = "INSERT INTO People (first_name, last_name, patronymic, face_photo) VALUES (%s, %s, %s, %s)"
                values = (first_name_entry.get(), last_name_entry.get(), patronymic_entry.get(), open(face_photo_path.get(), 'rb').read())
                cursor.execute(query, values)
                connection.commit()
                cursor.close()
                connection.close()
                first_name_entry.delete(0, END)
                last_name_entry.delete(0, END)
                patronymic_entry.delete(0, END)
                face_photo_path.set('')
                messagebox.showinfo("Успех", "Данные успешно добавлены в базу данных.")
            except Exception as e:
                messagebox.showerror("Ошибка")
        else:
            messagebox.showerror("Ошибка добавления данных", "Пожалуйста, заполните все поля.")

    add_button = Button(frame, text='Добавить', command=add_button_clicked, font=bold_font, bg="#87cefa", fg="black")
    add_button.grid(row=4, column=1)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

    return frame
