"""

Name: Shanie Portal
Date: 10/28/2024
Assignment: Module 9: SQLite3 Database
Due Date: 10/27/2024
About this project: Develop the database for a small scale real-world applications using third-party Python libraries
discussed in the course.
All work below was performed by Shanie Portal

"""
import sqlite3

if __name__ == '__main__':
    # Connect to database or create if doesn't exist.
    conn = sqlite3.connect("People.db")
    c = conn.cursor()

    # Delete one row but not all.
    c.execute("DELETE FROM People WHERE UserId = 3")

    # Update one row in the Entry table.
    c.execute("UPDATE Entry SET UserId = 2 WHERE UserId = 3")

    # Update: Update one row in the People table.
    c.execute("UPDATE People SET Name = 'UpdatedName' WHERE UserId = 1")

    conn.commit()

    # Select all rows and print them.
    c.execute("SELECT * FROM People")
    for row in c:
        print(row)

    # Select the Name column and print each name.
    c.execute("SELECT Name FROM People")
    for row in c:
        print(row)

    # Select all rows where UserId = 0 and print them.
    c.execute("SELECT * FROM People WHERE UserId = 0")
    for row in c:
        print(row)

    # Select Name column where UserId = 0 and print it.
    c.execute("SELECT Name FROM People WHERE UserId = 0")
    for row in c:
        print(row)

    # Close the connection.
    conn.close()
