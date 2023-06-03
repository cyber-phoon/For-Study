from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from edit_user import Edit_Windows
import tkinter as tk

class RequestWindowAD():
    def __init__(self):
        self.root = Tk()
        bold_font = ("Tahoma", 10, "bold")
        self.root.configure(bg="light blue")
        self.edit_window = None
        self.selected_fio = ""
        self.selected_data = None
        self.root.title("Редактирование запроса")
        self.root.geometry('1500x600')
        #self.root.resizable(False, False)

        Label(self.root, text='Статус принятия:', font=bold_font, bg="#87cefa", fg="black").grid(row=1, column=0, sticky=E)
        self.acceptance_status = ttk.Combobox(self.root, values=['В работе', 'Согласуется'], state="readonly")
        self.acceptance_status.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        Label(self.root, text='Статус завершения:', font=bold_font, bg="#87cefa", fg="black").grid(row=2, column=0, sticky=E)
        self.completed_status = ttk.Combobox(self.root, values=['Выполнена', 'Завершена'], state="readonly")
        self.completed_status.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        self.add_button = Button(self.root, text='Добавить', command=lambda: self.add_acceptance_button_clicked(), font=bold_font, bg="#87cefa", fg="black", width=22)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10, sticky=N)
        self.add_button.bind("<Enter>", self.on_enter)
        self.add_button.bind("<Leave>", self.on_leave)


        self.treeview = ttk.Treeview(self.root)
        self.treeview['show'] = 'headings'
        self.treeview['columns'] = ('request','action','fio', 'comment', 'acceptance_status', 'completion_status')
        #self.treeview.heading('id', text='ID')
        self.treeview.heading('request', text='Запрос')
        self.treeview.heading('action', text='Действие')
        self.treeview.heading('fio', text='ФИО')
        self.treeview.heading('comment', text='Комментарий')
        self.treeview.heading('acceptance_status', text='Статус принятия')
        self.treeview.heading('completion_status', text='Статус завершения')
        #self.treeview.column('id', width=50)
        self.treeview.column('request', width=300)
        self.treeview.column('action', width=150)
        self.treeview.column('fio', width=300)
        self.treeview.column('comment', width=150)
        self.treeview.column('acceptance_status', width=150)
        self.treeview.column('completion_status', width=150)
        self.treeview.grid(row=4, columnspan=2, padx=10, pady=10)

        Label(self.root).grid(row=5, column=0, sticky=W)
        self.selected_id = StringVar()
        self.selected_id_label = Label(self.root, textvariable=self.selected_id)
        self.selected_id_label.grid(row=5, column=1, padx=10, pady=10)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )

        self.cursor = self.conn.cursor()
        self.load_data()
        self.root.after(5000, self.update_data)
        self.treeview.bind("<<Button-1>>", self.add_acceptance_button_clicked)
        self.treeview.bind("<Double-Button-1>", self.treeview_select)

    def on_enter(self, event):
        event.widget.config(bg="white", fg="#87cefa")

    def on_leave(self, event):
        event.widget.config(bg="#87cefa", fg="black")
    def update_data(self):
        self.treeview.delete(*self.treeview.get_children())
        self.load_data()
        self.root.after(5000, self.update_data)

    def load_data(self):
        self.treeview.delete(*self.treeview.get_children())
        query = "SELECT request, action, fio, comment, acceptance_status, completion_status FROM requests"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            item = list(row)
            if item[4] == None: item[4] = 'На рассмотрении'
            if item[5] == None: item[5] = 'На рассмотрении'
            row = tuple(item)
            self.treeview.insert("", tk.END, values=row)



    def treeview_select(self, event):
        selected_item = self.treeview.focus()
        self.selected_data = self.treeview.item(selected_item)["values"]  # Сохранение выбранных данных
        if self.selected_data:
            self.selected_id.set(self.selected_data[0])
            fio = self.selected_data[2].split()  # Разделить ФИО на отдельные элементы
            self.open_edit_window(fio)
        else:
            self.selected_id.set("")

    def add_acceptance_button_clicked(self):
        selected_item = self.treeview.selection()
        if selected_item:
            request_id = self.treeview.item(selected_item, 'values')[0]
            accepted = self.acceptance_status.get()
            completed = self.completed_status.get()
            query = "UPDATE requests SET acceptance_status = %s, completion_status = %s WHERE request = %s"
            values = (accepted, completed, request_id)
            self.cursor.execute(query, values)
            self.conn.commit()
            self.update_data()
            self.completed_status.set('')
            self.acceptance_status.set('')

    def open_edit_window(self, fio):
        if self.edit_window is None:
            if fio != []:
                self.edit_window = Edit_Windows(fio)
            else:
                messagebox.showerror("Ошибка", "Отсутствует ФИО")
        #self.edit_window.set_fio(self.selected_data)  # Передача выбранных данных


    def run(self):
        self.root.mainloop()
