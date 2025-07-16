import sqlite3
from rich import print


conn = sqlite3.connect("aas_tutorial.db")
cur = conn.cursor()
table_name = 'aas_old_student_data'

cur.execute(f"SELECT * from {table_name} where student_name = 'Jonathan Porter'")
print(cur.fetchall())


cur.execute(f"SELECT * from {table_name} WHERE year = '2024' ORDER BY maths ASC LIMIT 5 ")
print(cur.fetchall())


cur.execute(f"SELECT * from {table_name} WHERE year = '2024' ORDER BY computer_science DESC LIMIT 5 ")
print(cur.fetchall())