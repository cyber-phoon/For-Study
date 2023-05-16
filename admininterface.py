import tkinter as tk
from tkinter import *
from add_photo import Add_Photo
import cv2
from add_person_in_users import Add_Persons_Window
from add_users_of_program import Users_Of_Program_Window
from DownloadWindow import Download_Window
#from edit_user import Edit_Windows
from RequestWindowAD import RequestWindowAD
#from showallpeople import ShowAllBd


class AdminWindow():
    def __init__(self, master, db_work):
        self.master = master
        self.master.title("Администрирование")
        self.master.geometry('810x430')
        self.master.resizable(False, False)
        self.db_work = db_work
        # self.error_button = tk.Button(self.master, text="Просмотр ошибок")
        # self.error_button.pack(anchor="w")

        self.photo_button = tk.Button(self.master, text="Создание учетной записи", command=self.add_photo, width=20)
        self.photo_button.pack(anchor="w", pady=(100, 5))

        self.add_person = tk.Button(self.master, text="Создание пропуска", command=self.create_person_window, width=20)
        self.add_person.pack(anchor="w", pady=5)

        self.download = tk.Button(self.master, text="Отчет рабочего времени", command=self.download_window, width=20)
        self.download.pack(anchor="w", pady=5)

        # self.download = tk.Button(self.master, text="Изменение данных", command=Edit_Windows)
        # self.download.pack(anchor="w")

        self.show_all_button = tk.Button(self.master, text="Запросы", command=self.request_window, width=20)
        self.show_all_button.pack(anchor="w", pady=5)

        # self.show_all_button = tk.Button(self.master, text="Показать пользователей")
        # self.show_all_button.pack(anchor="w")

    def add_photo(self):
        add_users = Users_Of_Program_Window()
        add_users.run()


    def create_person_window(self):
        persons_window = Add_Persons_Window()
        persons_window.run()

    def download_window(self):
        download_window = Download_Window()
        download_window.run()

    def request_window(self):
        RequestWindow = RequestWindowAD()
        RequestWindow.root.mainloop()

    #def edit_user(self):
        #edit_user = Edit_Windows()
        #edit_user.run()


#update_data = UpdateData()
#update_data.root.mainloop()


