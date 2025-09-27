import sqlite3

def init_db():
    conn = sqlite3.connect("verifier.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, pincode TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, address TEXT, pincode TEXT, assigned_employee INTEGER)")
    conn.commit()
    conn.close()

def get_employees():
    return [{"id": 1, "name": "Raj", "pincode": "110001"},
            {"id": 2, "name": "Asha", "pincode": "201301"}]

def get_customers():
    return [{"id": 101, "name": "Ravi Kumar", "pincode": "110001"},
            {"id": 102, "name": "Sunita Sharma", "pincode": "201301"}]

def assign_customers(customers, employees):
    results = []
    for c in customers:
        results.append({"customer": c["name"], "employee": employees[0]["name"]})
    return results
