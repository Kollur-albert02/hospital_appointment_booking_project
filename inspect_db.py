import sqlite3

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

print("TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

print("\nSCHEMA:")
cursor.execute("PRAGMA table_info(appointments);")
for col in cursor.fetchall():
    print(col)

print("\nDATA:")
cursor.execute("SELECT * FROM appointments;")
for row in cursor.fetchall():
    print(row)

conn.close()
