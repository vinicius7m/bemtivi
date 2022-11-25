import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="alunoaluno",

)

c = db.cursor()

c.execute("CREATE DATABASE IF NOT EXISTS bemtivi")

c.close()
db.close()