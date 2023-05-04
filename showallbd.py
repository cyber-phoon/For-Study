from tkinter import *
import mysql.connector


class ShowAll:
    def __init__(self):
        self.root = Tk()
        self.root.title("Список клиентов")
        self.root.geometry("800x600")

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )

        self.mycursor = self.mydb.cursor()

        self.mycursor.execute("SELECT id, first_name, last_name, patronymic, time FROM people")

        myresult = self.mycursor.fetchall()

        cols = ["ID", "Имя", "Фамилия", "Отчество", "Дата"]

        for i in range(len(cols)):
            e = Entry(self.root, width=20, fg='red')
            e.grid(row=0, column=i)
            e.insert(END, cols[i])

        for i in range(len(myresult)):
            for j in range(5):
                e = Entry(self.root, width=20, fg='blue')
                e.grid(row=i+1, column=j)
                e.insert(END, myresult[i][j])


#root = Tk()
#app = ShowAll(root)
#root.mainloop()
