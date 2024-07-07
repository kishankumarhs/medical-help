from dataclasses import dataclass
import mysql.connector
def connectDB():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kishan_123",
    database = 'help',
    port=9000
    )
    print(mydb)
    return mydb