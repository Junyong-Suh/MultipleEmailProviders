CREATE TABLE Logs (
	id INTEGER PRIMARY KEY,
	user_ip TEXT,
	user_agent TEXT,
	type TEXT,
	status_code TEXT,
	payload TEXT,
	response TEXT,
	provider TEXT,
	version TEXT,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
