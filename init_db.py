# init_db.py
# Create sqlite DB and tables
import sqlite3


DB = 'app_data.db'


def init():
conn = sqlite3.connect(DB)
cur = conn.cursor()


cur.execute('''
CREATE TABLE IF NOT EXISTS employees (
id INTEGER PRIMARY KEY AUTOINCREMENT,
employee_id TEXT UNIQUE,
name TEXT,
pincode TEXT,
lat REAL,
lon REAL,
capacity INTEGER DEFAULT 0,
password TEXT,
active INTEGER DEFAULT 1
);
''')


cur.execute('''
CREATE TABLE IF NOT EXISTS customers (
id INTEGER PRIMARY KEY AUTOINCREMENT,
cust_ref TEXT,
name TEXT,
address TEXT,
pincode TEXT,
lat REAL,
lon REAL,
status TEXT DEFAULT 'Pending',
assigned_employee_id TEXT,
created_at TEXT
);
''')


cur.execute('''
CREATE TABLE IF NOT EXISTS verification_reports (
id INTEGER PRIMARY KEY AUTOINCREMENT,
customer_id INTEGER,
employee_id TEXT,
verified_address TEXT,
photo_path TEXT,
status TEXT,
notes TEXT,
timestamp TEXT
);
''')


conn.commit()
conn.close()
print('init done')


if __name__ == '__main__':
init()
