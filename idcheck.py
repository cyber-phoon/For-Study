import mysql.connector
from tkinter import *
from tkinter import messagebox
from update_data import UpdateData
class IdCheck():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x100")
        self.root.title("Проверка ID")

        # Создаем метку и поле для ввода ID
        self.id_label = Label(self.root, text="Введите ID:")
        self.id_label.pack()
        self.id_entry = Entry(self.root)
        self.id_entry.pack()

        # Создаем кнопку для проверки ID
        self.check_button = Button(self.root, text="Проверить", command=self.check_id_button)
        self.check_button.pack()

    def check_id(self, id):
        cnx = mysql.connector.connect(user='root', password='qw123', host='localhost', database='diploma')
        cursor = cnx.cursor()
        query = ("SELECT id FROM people WHERE id = %s")
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cnx.close()
        return result is not None

    def check_id_button(self):
        id = self.id_entry.get()
        if self.check_id(id):
            # Если ID существует в базе данных, открываем новое окно
            cnx = mysql.connector.connect(user='root', password='qw123', host='localhost', database='diploma')
            cursor = cnx.cursor()
            query = ("SELECT id, first_name, last_name, patronymic, time, face_photo FROM people WHERE id = %s")
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            cnx.close()

            # Создаем новое окно и выводим все данные о человеке
            new_window = Toplevel(self.root)
            new_window.title("Данные о человеке")
            new_window.geometry("800x500")

            self.id_label = Label(new_window, text="ID: {}".format(result[0]))
            self.id_label.pack()
            self.first_name_label = Label(new_window, text="Имя: {}".format(result[1]))
            self.first_name_label.pack()
            self.last_name_label = Label(new_window, text="Фамилия: {}".format(result[2]))
            self.last_name_label.pack()
            self.patronymic_label = Label(new_window, text="Отчество: {}".format(result[3]))
            self.patronymic_label.pack()
            self.time_label = Label(new_window, text="Время: {}".format(result[4]))
            self.time_label.pack()

            # Передаем id в экземпляр класса UpdateData
            self.update_data = UpdateData(id)
            self.update_data.root.mainloop()
        else:
            # Если ID не найден, показываем сообщение об ошибке
            messagebox.showerror("Ошибка", "ID не существует в базе данных!")

    #def update_data(self):
        #update_data = UpdateData()
        #update_data.root.mainloop()

#app = IdCheck()
#app.root.mainloop()
