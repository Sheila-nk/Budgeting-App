import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (?, ?, ?, ?)",
            ('Sheila', 'Kahwai', 'kahwaisheila@gmail.com', '1234june')
            )
            
connection.commit()
connection.close() 