import sqlite3

# Connect to database (this will create hospital.db)
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create appointments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    health_condition TEXT NOT NULL,
    doctor_name TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database and appointments table created successfully!")
