from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

class RequestWindowAD():
    def __init__(self):
        self.root = Tk()
        self.root.title("Добавить запрос")
        self.root.geometry('1300x600')
        #self.root.resizable(False, False)

        Label(self.root, text='Статус принятия:').grid(row=1, column=0, sticky=W)
        self.acceptance_status = ttk.Combobox(self.root, values=['В работе', 'Согласуется'], state="readonly")
        self.acceptance_status.grid(row=1, column=1, padx=10, pady=10)

        Label(self.root, text='Статус завершения:').grid(row=2, column=0, sticky=W)
        self.completed_status = ttk.Combobox(self.root, values=['Выполнена', 'Завершена'], state="readonly")
        self.completed_status.grid(row=2, column=1, padx=10, pady=10)

        add_button = Button(self.root, text='Добавить', command=lambda: self.add_acceptance_button_clicked())
        add_button.grid(row=3, column=1)

        self.treeview = ttk.Treeview(self.root)
        self.treeview['columns'] = ('id', 'request','action','comment', 'acceptance_status', 'completion_status')
        self.treeview.heading('id', text='ID')
        self.treeview.heading('request', text='Запрос')
        self.treeview.heading('acceptance_status', text='Статус принятия')
        self.treeview.heading('completion_status', text='Статус завершения')
        self.treeview.heading('action', text='Действие')
        self.treeview.heading('comment', text='Комментарий')
        self.treeview.column('id', width=50)
        self.treeview.column('request', width=300)
        self.treeview.column('action',width=150)
        self.treeview.column('comment',width=150)
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
        self.treeview.bind("<<TreeviewSelect>>", self.treeview_select)

    def update_data(self):
        self.treeview.delete(*self.treeview.get_children())
        self.load_data()
        self.root.after(5000, self.update_data)

    def load_data(self):
        self.treeview.delete(*self.treeview.get_children())
        query = "SELECT id, request, action, comment, acceptance_status, completion_status FROM requests"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            self.treeview.insert("", "end", values=row)

    def treeview_select(self, event):
        selected_item = self.treeview.focus()
        data = self.treeview.item(selected_item)["values"]
        if data:
            self.selected_id.set(data[0])
            query = "UPDATE requests SET acceptance_status = %s, completion_status = %s WHERE id = %s"
            values = (self.acceptance_status.get(), self.completed_status.get(), data[0])
            self.cursor.execute(query, values)
            self.conn.commit()
        else:
            self.selected_id.set("")

    def add_acceptance_button_clicked(self):
        selected_item = self.treeview.selection()
        if selected_item:
            row = selected_item[0]
            request_id = self.treeview.item(row, 'values')[0]
            accepted = self.acceptance_status.get()
            completed = self.completed_status.get()
            if accepted or completed:
                query = "UPDATE requests SET acceptance_status = %s, completion_status = %s WHERE id = %s"
                values = (accepted, completed, request_id)
                self.cursor.execute(query, values)
                self.conn.commit()
                self.update_data()
                messagebox.showinfo("Успех", "Статус запроса успешно изменен!")
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, выберите статус принятия или завершения!")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите запрос для изменения статуса!")

    def run(self):
        self.root.mainloop()
