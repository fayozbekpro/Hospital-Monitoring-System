import sqlite3 as sq

class Database:
	def __init__(self):
		self.db = sq.connect("hospital.db")
		self.cur = self.db.cursor()

	def getTableResults(self, table_name):
		self.cur.execute(f"SELECT * FROM {table_name}")
		return self.cur.fetchall()

	def getTypeRooms(self, typed, equal):
		self.cur.execute(f"SELECT * FROM rooms WHERE {typed} = {equal}")
		return self.cur.fetchall()

	def getTypePatients(self, floor, floor_num, room, room_num):
		self.cur.execute(f"SELECT * FROM patients WHERE {floor} = {floor_num} AND {room} = {room_num}")
		return self.cur.fetchall()

	def insertPatient(self, name,surname, room_num, floor, room_type, registered_date):
		res = self.cur.execute(f"INSERT INTO patients VALUES(null, '{name}', '{surname}', '{room_num}', '{floor}', '{room_type}', '{registered_date}')")
		return self.cur.rowcount

	def insertRoom(self, room_num, floor, room_type, registered):
		self.cur.execute(f"INSERT INTO rooms VALUES(null, '{room_num}', '{floor}', '{room_type}', '{registered}')")
		return self.cur.rowcount

	def removePatient(self, identificator):
		self.cur.execute(f"DELETE FROM patients WHERE id='{identificator}'")
		return self.cur.rowcount


	def changeRoomRegistered(self, room_num, val):
		self.cur.execute(f"UPDATE rooms SET registered = '{val}' WHERE room_num = {room_num}")
		return self.cur.rowcount
	
	def insertAdmin(self, name, login, password, rank):
		self.cur.execute(f"INSERT INTO admins VALUES(null, '{name}', '{login}', '{password}', '{rank}')")
		return self.cur.rowcount

	def deleteAllinTable(self, table_name):
		self.cur.execute(f"DELETE FROM {table_name}")
	
	def executer(self, task):
		self.cur.execute(task)
		return self.cur.fetchall()
	def __enter__(self):
		# self.cur.execute(f"PRAGMA table_info(admins)")
		return self
	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.db.commit()
		self.db.close()

with Database() as db:
	for i in range(20,31):
		db.insertRoom(i, 3, "lux", "False")
