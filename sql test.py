import sqlite3

# 1. Connect to your specific database
db = sqlite3.connect('stellar diary.db')
cursor = db.cursor()

# 2. Execute the query to grab everything from the observation table
cursor.execute("SELECT * FROM observation")

# 3. Fetch all the rows into a list
all_logs = cursor.fetchall()

# 4. Loop through and print each row
if all_logs:
    print(f"Found {len(all_logs)} observations in the database:\n")
    for row in all_logs:
        print(row)
else:
    print("The database is currently empty. Go save some stars!")

# 5. Always close the connection when you're done
db.close()