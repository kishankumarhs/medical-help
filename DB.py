from dataclasses import dataclass
import mysql.connector
def connectDB():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = 'help'
    )
    print(mydb)
    return mydb