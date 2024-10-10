import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Retrieve data from the table
c.execute("SELECT * FROM core_weeklyapraverage;")

# Fetch all results
results = c.fetchall()

# Check if results are empty
if results:
    # Print the results if available
    for row in results:
        print(row)
else:
    print("No data found in core_weeklyapraverage.")

# Close the connection
conn.close()
