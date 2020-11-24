import sqlite3

<<<<<<< HEAD
print("Connected to the datebase baby!!")

print("Hello World")

=======
# Create table
c.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
c.execute("INSERT INTO stocks VALUES ('2007-02-01','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can close the connection right after making the commits
conn.close()
>>>>>>> 9a5b72a (Updated Database)
