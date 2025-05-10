import sqlite3
conn = sqlite3.connect("aas_tutorial.db")

cur = conn.cursor()
table_name = 'aas_old_student_data'

cur.execute(f"""CREATE TABLE IF NOT EXISTS  {table_name}(
    year INTEGER NOT NULL,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    english INTEGER NOT NULL,
    maths INTEGER NOT NULL,
    history INTEGER,
    computer_science INTEGER,
    science INTEGER NOT NULL,
    class_group TEXT, 
    PRIMARY KEY (student_id, year)
    );""")

cur.execute(f"PRAGMA table_info({table_name})") # PRAGMA is a special work used to check metadata (that is data about the data!)
print(cur.fetchall())

cur.execute(f"SELECT * from {table_name}")
print(cur.fetchall())