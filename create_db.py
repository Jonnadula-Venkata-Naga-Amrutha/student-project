import sqlite3

conn = sqlite3.connect('student.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll_no TEXT,
    branch TEXT,
    year TEXT,
    email TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    c_marks INTEGER,
    python_marks INTEGER,
    dbms_marks INTEGER,
    java_marks INTEGER,
    total INTEGER,
    percentage REAL,
    grade TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")