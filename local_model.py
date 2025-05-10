import requests
import pandas as pd
import sqlite3

data_per_year = []

years = ["2020", "2021", "2022", "2023", "2024"]
for year in years:
    response = requests.get(f"http://amoresa.eu/get-year/{year}")
    data_per_year.append(pd.read_json(response.text))

all_data_df = pd.concat(data_per_year)
print(all_data_df)


conn = sqlite3.connect("aas_tutorial.db")
table_name = "aas_old_student_data"
print(all_data_df.columns)


# Renaming columns to match the database schema
all_data_df = all_data_df.rename(
    columns={
        "Computer Science": "computer_science",
        "English": "english",
        "Group": "class_group",  # group is a reserved word in sql!
        "History": "history",
        "Maths": "maths",
        "Science": "science",
        "Student ID": "student_id",
        "Student Name": "student_name",
        "Year": "year",
    }
)




# DROPPING UNWANTED COLUMN
all_data_df = all_data_df.drop("Unnamed: 0", axis="columns")
print(all_data_df.columns)


#IDENTIFYING PRIMARY KEY DUPLICATES
duplicates_df = all_data_df[
    all_data_df.duplicated(keep=False, subset=["year", "student_id"])
]
print("HEAD OF DUPLICATES BEFORE DROPPING DUPLICATES") 
print(duplicates_df.head()) #Just to see the duplicates


# DROPPING DUPLICATES
all_data_df = all_data_df.drop_duplicates(subset=["year", "student_id"])

# CHEKCING DUPLICATES ARE GONE (NOT NEEDED)
duplicates_df = all_data_df[all_data_df.duplicated(keep=False, subset=["year", "student_id"])]
print("HEAD OF DUPLICATES AFTER DROPPING DUPLICATES")
print(duplicates_df.head())



# ## FINDING OUT IF THERE ARE EMPTY VALUES

missing_rows = all_data_df[all_data_df.isnull().any(axis=1)]
print([all_data_df.isnull().any(axis=1)])

print("ROWS WITH MISSING VALUES")
print(missing_rows)


all_data_df = all_data_df.dropna(
    axis=0,
    subset=[
        "english",
        "maths",
        "class_group",
        "science",
        "student_id",
        "student_name",
        "year",
    ],
)

#Printing the rows with missing values again to see if they are gone
missing_rows = all_data_df[all_data_df.isnull().any(axis=1)]
print("ROWS WITH MISSING VALUES")
print(missing_rows.head())

all_data_df.to_sql(table_name, conn, if_exists="replace", index=False)

cur = conn.cursor()
cur.execute(f"SELECT * from {table_name}")
print(cur.fetchall())

