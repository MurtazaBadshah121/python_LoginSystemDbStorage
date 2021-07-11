import sqlite3

with sqlite3.connect("user.db") as db:
    cursor = db.cursor()


# This statement creates the database tables
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS user(
# user_ID INTEGER PRIMARY KEY,
# Email VARCHAR(20) NOT NULL,
# password VARCHAR(20) NOT NULL,
# access_Count INTEGER DEFAULT 0)
# ''')

# This statement is used to enter values into the table for testing
# cursor.execute('''
# INSERT INTO user(Email, password)
# VALUES("mb", "12345")
# ''')

# This statement deletes the table
# cursor.execute('''
# DROP table user
# ''')

# This statement deletes all data from user table
# cursor.execute('''DELETE FROM user''')

db.commit()

cursor.execute('''
SELECT * FROM user
''')

print(cursor.fetchall())