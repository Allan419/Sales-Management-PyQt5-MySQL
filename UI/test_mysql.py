import mysql.connector

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    passwd = "Zzl33221144"
)

print(mydb)