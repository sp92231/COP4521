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
    conn = sqlite3.connect("People.db")
    c = conn.cursor()

    # Enable foreign keys support.
    c.execute("PRAGMA foreign_keys = ON")

    # Drop the Entry table if it exists.
    c.execute("DROP TABLE IF EXISTS Entry")

    # Create Entry table.
    c.execute(
        """CREATE TABLE Entry(
            EntryId INTEGER PRIMARY KEY, 
            UserId INTEGER, 
            NameOfBakingItem TEXT, 
            NumExcellentVotes INTEGER, 
            NumOkVotes INTEGER, 
            NumBadVotes INTEGER,
            FOREIGN KEY (UserId) REFERENCES People(UserId)
        )"""
    )

    # Insert values into Entry table.
    c.execute(
        "INSERT INTO Entry (EntryId, UserId, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes) VALUES (0, 1, 'Pie', 5, 0, 4)")  # UserId 1
    c.execute(
        "INSERT INTO Entry (EntryId, UserId, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes) VALUES (1, 2, 'Pudding', 3, 1, 1)")  # UserId 2
    c.execute(
        "INSERT INTO Entry (EntryId, UserId, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes) VALUES (2, 3, 'Cake', 5, 0, 1)")  # UserId 3
    c.execute(
        "INSERT INTO Entry (EntryId, UserId, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes) VALUES (3, 4, 'Fudge', 2, 3, 0)")  # UserId 4

    # Commit the changes.
    conn.commit()

    # Display the results from the Entry table.
    c.execute("SELECT * FROM Entry")
    for row in c:
        print(row)

    # Close connection.
    conn.close()
