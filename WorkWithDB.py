import hashlib
class DB_Work():

	def __init__(self, conn, cursor):
		self.conn = conn
		self.cursor = cursor

	#Work with profiles#

	def show_profile_by_username_and_password(self, username, password):
		hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
		self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
							(username, hashed_password))
		profile = self.cursor.fetchone()
		return profile

