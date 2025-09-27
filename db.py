# db.py
# Simple SQLite helpers for this app
import sqlite3
from datetime import datetime


DB = 'app_data.db'


def get_conn():
return sqlite3.connect(DB, check_same_thread=False)


# Employee CRUD


def upsert_employee(emp):
conn = get_conn(); cur = conn.cursor()
cur.execute('SELECT id FROM employees WHERE employee_id=?', (emp['employee_id'],))
row = cur.fetchone()
if row:
cur.execute('''UPDATE employees SET name=?, pincode=?, lat=?, lon=?, capacity=?, password=?, active=? WHERE employee_id=?''',
(emp.get('name'), emp.get('pincode'), emp.get('lat'), emp.get('lon'), emp.get('capacity', 0), emp.get('password', ''), emp.get('active',1), emp['employee_id']))
else:
cur.execute('''INSERT INTO employees (employee_id, name, pincode, lat, lon, capacity, password, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
(emp['employee_id'], emp.get('name'), emp.get('pincode'), emp.get('lat'), emp.get('lon'), emp.get('capacity',0), emp.get('password',''), emp.get('active',1)))
conn.commit(); conn.close()


def list_employees():
conn = get_conn(); cur = conn.cursor()
cur.execute('SELECT employee_id, name, pincode, lat, lon, capacity, active FROM employees')
rows = cur.fetchall(); conn.close()
cols = ['employee_id','name','pincode','lat','lon','capacity','active']
return [dict(zip(cols, r)) for r in rows]


def get_employee_by_id(emp_id):
conn = get_conn(); cur = conn.cursor()
cur.execute('SELECT employee_id, name, pincode, lat, lon, capacity, active FROM employees WHERE employee_id=?', (emp_id,))
r = cur.fetchone(); conn.close()
if not r: return None
cols = ['employee_id','name','pincode','lat','lon','capacity','active']
return dict(zip(cols, r))


# Customers


def bulk_insert_customers(list_of_dicts):
conn = get_conn(); cur = conn.cursor()
for c in list_of_dicts:
cur.execute('''INSERT INTO customers (cust_ref, name, address, pincode, lat, lon, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
(c.get('cust_ref'), c.get('name'), c.get('address'), c.get('pincode'), c.get('lat'), c.get('lon'), 'Pending', datetime.utcnow().isoformat()))
conn.commit(); conn.close()


def fetch_unassigned_customers():
conn = get_conn(); cur = conn.cursor()
cur.execute("SELECT id, cust_ref, name, address, pincode, lat, lon FROM customers WHERE assigned_employee_id IS NULL AND status='Pending'")
rows = cur.fetchall(); conn.close()
cols = ['id','cust_ref','name','address','pincode','lat','lon']
return [dict(zip(cols,r)) for r in rows]


def assign_customer(customer_id, employee_id):
conn = get_conn(); cur = conn.cursor()
cur.execute('UPDATE customers SET assigned_employee_id=? WHERE id=?', (employee_id, customer_id))
conn.commit(); conn.close()


def fetch_customers_by_employee(employee_id):
conn = get_conn(); cur = conn.cursor()
cur.execute('SELECT id, cust_ref, name, address, pincode, lat, lon, status FROM customers WHERE assigned_employee_id=?', (employee_id,))
rows = cur.fetchall(); conn.close()
cols = ['id','cust_ref','name','address','pincode','lat','lon','status']
return [dict(zip(cols,r)) for r in rows]


def update_customer_status(customer_id, status):
conn = get_conn(); cur = conn.cursor()
cur.execute('UPDATE customers SET status=? WHERE id=?', (status, customer_id))
conn.commit(); conn.close()


# Verification reports


def save_report(customer_id, employee_id, verified_address, photo_path, status, notes=None):
conn = get_conn(); cur = conn.cursor()
cur.execute('INSERT INTO verification_reports (customer_id, employee_id, verified_address, photo_path, status, notes, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
(customer_id, employee_id, verified_address, photo_path, status, notes, datetime.utcnow().isoformat()))
conn.commit(); conn.close()


def list_reports():
conn = get_conn(); cur = conn.cursor()
cur.execute('SELECT id, customer_id, employee_id, verified_address, photo_path, status, notes, timestamp FROM verification_reports ORDER BY timestamp DESC')
rows = cur.fetchall(); conn.close()
cols = ['id','customer_id','employee_id','verified_address','photo_path','status','notes','timestamp']
return [dict(zip(cols,r)) for r in rows]
