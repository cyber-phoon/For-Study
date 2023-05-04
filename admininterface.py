import tkinter as tk
from tkinter import *
from add_photo import Add_Photo
import cv2
from add_person_in_users import Add_Persons_Window
from add_users_of_program import Users_Of_Program_Window
from DownloadWindow import Download_Window
from idcheck import IdCheck
from showallbd import ShowAll


class AdminWindow():
    def __init__(self, master, db_work):
        self.master = master
        self.master.title("Администрирование")
        self.master.geometry('810x430')
        self.db_work = db_work
        #self.error_button = tk.Button(self.master, text="Просмотр ошибок")
        #self.error_button.pack()
        self.photo_button = tk.Button(self.master, text="Создание учетной записи", command=self.add_photo)
        self.photo_button.pack()
        self.add_person = tk.Button(self.master, text="Создание пропуска", command=self.create_person_window)
        self.add_person.pack()
        self.download = tk.Button(self.master, text="Отчет рабочего времени", command=self.download_window)
        self.download.pack()
        self.download = tk.Button(self.master, text="Изменение данных", command=self.update_data)
        self.download.pack()
        self.show_all_button = tk.Button(self.master, text="Просмотреть всех клиентов", command=self.showallbd)
        self.show_all_button.pack()

    def add_photo(self):
        add_users = Users_Of_Program_Window()
        add_users.run()


    def create_person_window(self):
        persons_window = Add_Persons_Window()
        persons_window.run()

    def download_window(self):
        download_window = Download_Window()
        download_window.run()

    def update_data(self):
        idcheck = IdCheck()
        idcheck.root.mainloop()

    def showallbd(self):
        showallbd = ShowAll()
        showallbd.root.mainloop()


#update_data = UpdateData()
#update_data.root.mainloop()


