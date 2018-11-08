import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS entrys (competicao text, atleta text, value real, unidade text)"
cursor.execute(create_table)
cursor.execute("INSERT INTO entrys VALUES ('100m', 'Shaq Moahmed', 10.99, 's')")

#ToDo fix types
create_table = "CREATE TABLE IF NOT EXISTS competitions (competicao text, ranking INTEGER, isFinished BOOLEAN, numTrys INTEGER)"
cursor.execute(create_table)
cursor.execute("INSERT INTO competitions VALUES ('100m', 1, 0, 1)")

connection.commit()
connection.close()