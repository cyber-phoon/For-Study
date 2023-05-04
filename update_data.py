import mysql.connector
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
import tempfile

class UpdateData():
    def __init__(self, id):
        # Подключаемся к базе данных
        conn = mysql.connector.connect(user='root', password='qw123', host='localhost', database='diploma')
        self.cursor = conn.cursor()

        # Создаем окно приложения и элементы интерфейса
        self.root = Tk()
        self.root.title("Редактирование данных о человеке")
        self.root.geometry("500x400")

        # Добавляем элементы интерфейса для ввода ФИО и фото
        self.id = Label(self.root, text="ID:")
        self.id.pack()
        self.id_entry = Entry(self.root)
        self.id_entry.insert(0, id)  # устанавливаем значение id по умолчанию
        self.id_entry.configure(state='readonly')
        self.id_entry.pack()

        # Добавляем элементы интерфейса для ввода ФИО и фото
        first_name_label = Label(self.root, text="Имя:")
        first_name_label.pack()
        self.first_name_entry = Entry(self.root)
        self.first_name_entry.pack()

        last_name_label = Label(self.root, text="Фамилия:")
        last_name_label.pack()
        self.last_name_entry = Entry(self.root)
        self.last_name_entry.pack()

        patronymic_label = Label(self.root, text="Отчество:")
        patronymic_label.pack()
        self.patronymic_entry = Entry(self.root)
        self.patronymic_entry.pack()

        photo_label = Label(self.root, text="Фото:")
        photo_label.pack()
        self.photo_path = None  # переменная для хранения пути к выбранному файлу фото
        photo_button = Button(self.root, text="Выбрать фото", command=self.choose_photo)
        photo_button.pack()

        take_photo_button = Button(self.root, text="Сделать фото", command=self.take_photo)
        take_photo_button.pack()

        # Добавляем кнопку "Проверить данные"
        check_button = Button(self.root, text="Проверить данные", command=self.check_data)
        check_button.pack()



    def choose_photo(self):
        # Выбираем файл фото и сохраняем его путь в переменной photo_path
        self.photo_path = filedialog.askopenfilename()

        # Открываем фото и читаем бинарные данные
        with open(self.photo_path, "rb") as image_file:
            self.face_photo_data = image_file.read()

        # Открываем фото
        self.face_photo = Image.open(self.photo_path)

    def take_photo(self):
        global photo_path  # Объявляем переменную photo_path как глобальную
        # Инициализируем камеру
        camera = cv2.VideoCapture(0)

        # Считываем кадр изображения
        ret, frame = camera.read()

        # Отображаем изображение в новом окне
        cv2.imshow('photo', frame)
        cv2.waitKey(0)

        # Сохраняем фотографию как временный файл
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            cv2.imwrite(tmp_file.name, frame)
            self.photo_path = tmp_file.name

        # Освобождаем ресурсы
        camera.release()
        cv2.destroyAllWindows()

    def check_data(self):
        # Получаем значения из полей ввода
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        patronymic = self.patronymic_entry.get()
        id_value = self.id_entry.get()

        # Получаем путь к выбранному фото
        face_photo = self.photo_path

        # Проверяем, что фото было выбрано
        if not face_photo:
            messagebox.showerror("Ошибка", "Выберите фото")
            return

        # Проверяем, что все поля были заполнены
        if not all([first_name, last_name, patronymic]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        # Подключаемся к базе данных
        conn = mysql.connector.connect(user='root', password='qw123', host='localhost', database='diploma')
        cursor = conn.cursor()

        # Ищем запись о человеке в БД по ФИО
        query = "SELECT id FROM people WHERE first_name=%s AND last_name=%s AND patronymic=%s"
        cursor.execute(query, (first_name, last_name, patronymic))
        result = cursor.fetchone()

        # Если не найдены данные о человеке с таким ФИО, выводим ошибку
        if not result:
            messagebox.showerror("Ошибка", "Данные о человеке не найдены в базе данных!")
            return

        # Получаем ID человека
        person_id = result[0]

        # Обновляем данные человека в БД
        query = "UPDATE people SET first_name=%s, last_name=%s, patronymic=%s, face_photo=%s WHERE id=%s"
        cursor.execute(query, (first_name, last_name, patronymic, face_photo, person_id))
        conn.commit()

        messagebox.showinfo("Успех", "Данные о человеке успешно обновлены в базе данных!")

#update_data = UpdateData()
#update_data.root.mainloop()