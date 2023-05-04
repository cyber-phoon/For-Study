import mysql.connector

class DB():

	def get_conn_and_cursor(self):
		self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )
		self.db_cursor = self.db_connection.cursor()
		return self.db_connection, self.db_cursor