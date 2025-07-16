import requests
import pandas as pd
import sqlite3
from rich import print

 # CREATING THE DATABASE AND TABLE
conn = sqlite3.connect("aas_tutorial.db")
cur = conn.cursor()
table_name = 'aas_old_student_data'

cur.execute(f"""CREATE TABLE IF NOT EXISTS  {table_name}(
    year INTEGER NOT NULL,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    maths INTEGER NOT NULL,
    computer_science INTEGER,
    class_group TEXT, 
    PRIMARY KEY (student_id, year)
    );""")

# PRAGMA is a special word used to check 
# metadata (that is data about the data!)
cur.execute(f"PRAGMA table_info({table_name})") 
print(cur.fetchall())

cur.execute(f"SELECT * from {table_name}")
print(cur.fetchall())



# response = requests.get("http://amoresa.eu/get-year/2020")
# student_data_df = pd.read_json(response.text)
# print(student_data_df)
      

# years = ['2020','2021', '2022', '2023', '2024']
# for year in years:
#     response = requests.get(f'http://amoresa.eu/get-year/{year}')
#     student_data_df = pd.read_json(response.text)
#     print(student_data_df)




years = ['2020','2021', '2022', '2023', '2024']
data_per_year = []
for year in years:
    response = requests.get(f'http://amoresa.eu/get-year/{year}')
    student_data_df = pd.read_json(response.text)
    data_per_year.append(student_data_df)

#CONCATENATE ALL DATAFRAMES
all_data_df = pd.concat(data_per_year)


#RENAME COLUMNS
all_data_df = all_data_df.rename(
    columns={
        "Computer Science": "computer_science",
        "Group": "class_group",  # group is a reserved word in sql!
        "Maths": "maths",
        "Student ID": "student_id",
        "Student Name": "student_name",
        "Year": "year",
    }
)


# #DROP UNWANTED COLUMN
all_data_df = all_data_df.drop("Unnamed: 0", axis="columns")
print(all_data_df.columns)


# DROP ROWS WITH MISSING MATHS VALUES
all_data_df = all_data_df.dropna(subset=['maths'], axis=0)


all_data_df.to_sql(table_name, conn, if_exists='append', index=False)

all_data_df.plot(kind='bar', x='year', y='maths', title='Maths Scores by Year')