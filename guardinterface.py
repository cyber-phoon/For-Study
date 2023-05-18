import tkinter as tk
import os
import datetime
import csv
import subprocess
from tkinter import simpledialog
from requestsbyguard import RequestGU


class GuardWindow():

    def __init__(self, master, db_work):
        self.master = master
        self.master.title("Приложение")
        self.master.geometry('810x430')
        self.db_work = db_work
        self.master.configure(bg="light blue")
        bold_font = ("Tahoma", 10, "bold")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Создание кнопки "Запуск"
        self.button = tk.Button(self.master, text='Запуск', width=20, borderwidth=3, command=self.open_file,
                                font=bold_font, bg="#87cefa", fg="black")
        self.button.grid(row=2, column=1, padx=10, pady=10, sticky='se')
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

        # Создание кнопки "Добавить запрос"
        self.add_request = tk.Button(self.master, text='Добавить запрос', width=20, borderwidth=3,
                                     command=self.guardGU, font=bold_font, bg="#87cefa", fg="black")
        self.add_request.grid(row=2, column=0, padx=10, pady=10, sticky='se')
        self.add_request.bind("<Enter>", self.on_enter)
        self.add_request.bind("<Leave>", self.on_leave)

        # Создание и обновление часов
        self.clock_label = tk.Label(self.master, font=('Arial', 18), bg='white', fg='black')
        self.clock_label.grid(row=1, column=1, padx=10, pady=10, sticky='ne')
        self.update_clock()


        # Создание кнопки "Выход"
        self.quit_button = tk.Button(self.master, text='Выход', width=20, borderwidth=3, command=self.quit_app,
                                     font=bold_font, bg="#87cefa", fg="black")
        self.quit_button.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.quit_button.bind("<Enter>", self.on_enter)
        self.quit_button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget.config(bg="white", fg="#87cefa")

    def on_leave(self, event):
        event.widget.config(bg="#87cefa", fg="black")

    def open_file(self):
        subprocess.Popen(['python', 'engine.py'])

    def update_clock(self):
        now = datetime.datetime.now()
        self.clock_label.config(text=now.strftime('%H:%M:%S'))
        self.master.after(1000, self.update_clock)

    def guardGU(self):
        guardGU = RequestGU()
        guardGU.root.mainloop()

    def quit_app(self):
        self.master.destroy()
