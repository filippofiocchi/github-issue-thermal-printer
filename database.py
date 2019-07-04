import sqlite3
import os
connection = sqlite3.connect(os.environ['DATABASE_NAME'])
cursor = connection.cursor()


cursor.execute('''CREATE TABLE os.environ['DATABASE_NAME']
            (urls text)''')
connection.commit()
connection.close()

