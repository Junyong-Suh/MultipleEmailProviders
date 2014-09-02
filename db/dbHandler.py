import sqlite3
from os.path import isfile, getsize

class DbHandler:

	def initialize(self, dbPath):
		self.conn = sqlite3.connect(dbPath)
		self.c = conn.cursor()
		if self._isSQLite3(dbPath):
			print dbPath +" already exist."
		else:
			self._createDb(dbPath)
			print dbPath +" created."

	# ToDo: Error handlings needed
	def _createDb(self, dbPath):
		c.execute('''CREATE TABLE Logs (id INTEGER PRIMARY KEY, user_ip TEXT, user_agent TEXT, type TEXT, status_code TEXT, payload TEXT, response TEXT, provider TEXT, version TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
		conn.commit()

	# check if the file is SQLite3 DB
	# http://stackoverflow.com/questions/12932607/how-to-check-with-python-and-sqlite3-if-one-sqlite-database-file-exists
	def _isSQLite3(filename):
		if not isfile(filename):
			return False
		# SQLite database file header is 100 bytes
		if getsize(filename) < 100:
			return False
		else:
			fd = open(filename, 'rb')
			Header = fd.read(100)
			fd.close()

		if Header[0:16] == 'SQLite format 3\000':
			return True
		else:
			return False

	def writeJSONtoDB(self, jsonLog):
		if not _isValidJson(jsonLog):
			return False

		# inserting a row of data
		# logType=Log, v=v0.01, env=dev, statusCode=200, response={"message":"success"}, ip=127.0.0.1, userAgent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36, payload={"body": "<h1>Hello</h1><p>from Uber</p>", "from_name": "Uber", "from": "no-reply@uber.com", "to": "junyongsuh@gmail.com", "to_name": "Junyong Suh", "safeBody": "Hellofrom Uber", "subject": "Your Monday evening trip with Uber"}
		# c.execute("INSERT INTO Logs VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
		conn.commit()
