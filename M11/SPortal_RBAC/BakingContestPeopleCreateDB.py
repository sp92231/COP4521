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
    c.execute("drop table if exists People")
    # Create People table.
    c.execute(
        """CREATE TABLE People(
            UserId INTEGER PRIMARY KEY NOT NULL, 
            Name TEXT NOT NULL, 
            Age INT NOT NULL, 
            PhNum TEXT NOT NULL, 
            SecurityLevel INT NOT NULL, 
            LoginPassword TEXT NOT NULL
        )"""
    )
    # Insert data into People table.
    c.execute("INSERT INTO People VALUES (1,'PDiana', '34','123-675-7645', 1,'test123')")
    c.execute("INSERT INTO People VALUES (2, 'TJones', '68', '895-345-6523', 2, 'test123')")
    c.execute("INSERT INTO People VALUES (3, 'AMath', '29', '428-197-3967', 3, 'test123')")
    c.execute("INSERT INTO People VALUES (4, 'BSmith', '37', '239-567-3498', 2, 'test123')")
    conn.commit()

    # Select and display rows from People table.
    c.execute("Select * from People")
    for row in c:
        print(row)

    # Close connection.
    conn.close()
