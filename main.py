import csv
import sqlite3
import sys
import pandas as pd
import re

# For email validation
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


# for creating the Cypher dictionary
df = pd.read_excel("cypher.xlsx", index_col=0)
df = df.where(pd.notnull(df), None)
dict = df.to_dict()["converted_letters"]

# Converting all encryption key values into strings
keys_values = dict.items()
new_dict = {str(key) : str(value) for key, value in keys_values}

# This function logs and saves copies of every user that tries to login.
def hotBackup():
    with sqlite3.connect('user.db') as db:
            cursor = db.cursor()

    # Write to the csv file
    ###########################################################
    cursor.execute("SELECT email, access_Count FROM user")
    with open("usersdb-backup.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    ############################################################

# Login function used to log into the system.
def login():
    while True:
        email = input("Please enter a valid Email: ")

        if(re.search(regex, email)):
            password = input("Please enter your password: ").upper()
            encrypted = ""

            for letter in password:
                if letter in new_dict:
                    encrypted += new_dict[letter]
                else:
                    encrypted += letter


            with sqlite3.connect('user.db') as db:
                cursor = db.cursor()

            find_user = "SELECT * FROM USER WHERE Email = ? AND password = ?"
            cursor.execute(find_user, [(email), (encrypted)])

            results = cursor.fetchall()

        # UPDATE TableName SET TableField = TableField + 1 WHERE SomeFilterField = @ParameterID
            if results:
                for i in results:
                    print("Welcome " + i[1])
                    output = '''UPDATE user SET access_Count = access_Count + 1 WHERE Email = ?'''
                    cursor.execute(output, [(email)])
                    db.commit()
                    hotBackup()
                menu()

            else:
                print("Username and password not recognized")
                again = int(input("View main menu or exit? (1 = Main Menu / 2 = Exit): "))
                if again == 1:
                    menu()
                if again == 2:
                    print("Goodbye!")
                    sys.exit(1)
        else:
            print("Invalid email, Please enter a valid email address!")

# This function registers a new user
def newUser():
    found = 0
    while found == 0:
        email = input("Please enter your Email: ")
        if(re.search(regex, email)):

            with sqlite3.connect('user.db') as db:
                cursor = db.cursor()

            find_user = ("SELECT * FROM user WHERE EMAIL == ?")
            cursor.execute(find_user, [(email)])

            if cursor.fetchall():
                print("Email exists, please use a different email!")

            else:
                found = 1
                password = str(input("Please enter your password: ")).upper()
                encrypted = ""

                for letter in password:
                    if letter in new_dict:
                        encrypted += new_dict[letter]
                    else:
                        encrypted += letter
        else:
            print("Invalid email, Please enter a valid email address!")

    insertData = '''INSERT INTO user(Email, password) VALUES(?, ?)'''
    cursor.execute(insertData, [(email), (encrypted)])
    db.commit()


    hotBackup()
    menu()

# Main menu function
def menu():
    while True:
        print("====================================================")
        print("-----Welcome to the login platform!-----------------")
        print("****************************************************")
        print("  Please read the instructions carefully.           ")
        print("*****   1. Create New User                     *****")
        print("*****   2. Login to System with existing user? *****")
        print("*****   3. Exit                                *****")
        print("****************************************************")

        selection = input("Please enter the appropriate number for the option: ")

        if selection == "1":
            newUser()
        elif selection == "2":
            login()
        elif selection == "3":
            print("Goodbye!")
            sys.exit(1)
        else:
            print("Incorrect input please try again!")

# This function starts the application
def start():
    result = input("Welcome! Are you a new user? (Y/N): ")

    if result == 'y' or result == 'Y':
        newUser()
    elif result == 'n' or result == 'N':
        login()
    else:
        print("Incorrect input please try again!")
        start()

if __name__ == "__main__":
    start()