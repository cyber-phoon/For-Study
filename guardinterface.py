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

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.button = tk.Button(self.master, text='Запуск', width=20, borderwidth=3, command=self.open_file)
        self.button.grid(row=2, column=1, padx=10, pady=10, sticky='se')
        self.qweasd = tk.Button(self.master, text='Добавить запрос', width=20, borderwidth=3, command=self.guardGU)
        self.qweasd.grid()

        self.clock_label = tk.Label(self.master, font=('Arial', 18), bg='white', fg='black')
        self.clock_label.grid(row=1, column=1, padx=10, pady=10, sticky='ne')

        self.update_clock()

        self.text_frame = tk.Frame(self.master)
        self.text_frame.grid(row=1, column=0, sticky="nsew")
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        self.text_widget = tk.Text(self.text_frame)
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.text_widget.grid_rowconfigure(0, weight=1)
        self.text_widget.grid_columnconfigure(0, weight=1)

        #self.update_attendance(self.text_widget)

        self.quit_button = tk.Button(self.master, text='Выход', width=20, borderwidth=3, command=self.quit_app)
        self.quit_button.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)


    def open_file(self):
        subprocess.Popen(['python', 'engine.py'])

    def update_clock(self):
        now = datetime.datetime.now()
        self.clock_label.config(text=now.strftime('%H:%M:%S'))
        self.master.after(1000, self.update_clock)


    def guardGU(self):
        guardGU = RequestGU()
        guardGU.root.mainloop()

    #def update_attendance(self, text_widget):
        #with open('recognition.log', 'r') as csv_file:
            #text = csv_file.read()
        #self.text_widget.delete('1.0', tk.END)
        #self.text_widget.insert(tk.END, text)





    def quit_app(self):
        self.master.destroy()