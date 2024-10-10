import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Define your date ranges
start_date = datetime(2023, 12, 21)
end_date = datetime(2023, 12, 27)
target_start_date = datetime(2023, 12, 1)

# Calculate the number of days to loop through
num_days = (end_date - start_date).days + 1

for i in range(num_days):
    current_date = start_date + timedelta(days=i)
    target_date = target_start_date + timedelta(days=i)

    # Formulate the INSERT command
    insert_cmd = f"""
    INSERT INTO core_aprsave (validator, apr, key, date)
    SELECT validator, apr, key, '{target_date.strftime('%Y-%m-%d')} ' || substr(date, 12)
    FROM core_aprsave
    WHERE date(date) = '{current_date.strftime('%Y-%m-%d')}';
    """

    # Execute the command
    c.execute(insert_cmd)

# Commit the changes and close the connection
conn.commit()
conn.close()
