import tkinter as tk
from tkinter import ttk
from add_photo import Add_Photo
from add_person_in_users import create_add_persons_widgets
from add_users_of_program import create_users_program_widgets
from DownloadWindow import create_download_window
from RequestWindowAD import RequestWindowAD

class AdminWindow():
    def __init__(self, master, db_work):
        self.master = master
        bold_font = ("Tahoma", 10, "bold")
        self.master.configure(bg="light blue")
        self.master.title("Администрирование")
        self.master.geometry('810x430')
        self.master.resizable(False, False)
        self.db_work = db_work

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True)

        self.photo_frame = ttk.Frame(self.notebook)
        self.photo_frame.configure(style="My.TFrame")
        self.notebook.add(self.photo_frame, text='Создание учетной записи')

        self.add_person_frame = ttk.Frame(self.notebook)
        self.add_person_frame.configure(style="My.TFrame")
        self.notebook.add(self.add_person_frame, text='Создание пропуска')

        self.download_frame = ttk.Frame(self.notebook)
        self.download_frame.configure(style="My.TFrame")
        self.notebook.add(self.download_frame, text='Отчет рабочего времени')

        self.request_frame = ttk.Frame(self.notebook)
        self.request_frame.configure(style="My.TFrame")
        self.notebook.add(self.request_frame, text='Запросы')

        self.show_all_button = tk.Button(self.request_frame, text="Запросы", command=self.request_window, font=bold_font, bg="#87cefa", fg="black", width=22)
        self.show_all_button.pack(anchor="w", pady=3)
        self.show_all_button.bind("<Enter>", self.on_enter)
        self.show_all_button.bind("<Leave>", self.on_leave)

        style = ttk.Style()
        style.configure("My.TFrame", background="light blue")

        # Create the contents of the add_users_of_program file
        users_program_widgets = create_users_program_widgets(self.photo_frame)
        users_program_widgets.pack()

        # Create the contents of the add_person_in_users file
        persons_widgets = create_add_persons_widgets(self.add_person_frame)
        persons_widgets.pack()

        # Create the contents of the add_person_in_users file
        download_widgets = create_download_window(self.download_frame)
        download_widgets.pack()

    def on_enter(self, event):
        event.widget.config(bg="white", fg="#87cefa")

    def on_leave(self, event):
        event.widget.config(bg="#87cefa", fg="black")

    def add_photo(self):
        add_photo_window = Add_Photo(self.master, self.db_work)
        add_photo_window.run()

    def create_person_window(self):
        add_persons_window = create_add_persons_widgets()
        add_persons_window.run()

    def download_window(self):
        download_window = create_download_window(self.master)
        download_window.open_window()

    def request_window(self):
        request_window = RequestWindowAD()
        request_window.run()
