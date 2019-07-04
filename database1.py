import sqlite3
connection = sqlite3.connect('database1.db')
c = connection.cursor()

#Create table
c.execute('''CREATE TABLE database1
            (urls text)''')


#insert_url(url1)
#insert_url(url1)
#connection.commit()
#def get_url(url1):
# #



#def insert_url(url):
#    c.execute(" INSERT INTO database4 VALUES (?)",(url,))


# Save (commit) the changes
connection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
connection.close()

