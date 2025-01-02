import sqlite3

DATABASE_FILE = './tasks.db'

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Execute the SQL commands
# query = "DROP TABLE tasks;"
# cursor.execute(query)

# # Fetch all the results
# results = cursor.fetchall()
# for row in results:
#     print(row)

# Close the connection
cursor.close()
conn.close()
