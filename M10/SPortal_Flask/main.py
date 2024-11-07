"""

Name: Shanie Portal
Date: 11/03/2024
Assignment: Module 10: Basic Flask Website
Due Date: 11/03/2024
About this project: Develop the database for a small scale real-world applications using third-party Python libraries
discussed in the course.
All work below was performed by Shanie Portal

"""

from flask import Flask, render_template, request
import sqlite3 as sql
import os

# Create Flask instance.
app = Flask(__name__)
# Define database.
db_file = 'People.db'

# Check if database already exists. If not, create it.
if not os.path.exists(db_file):
    with open('BakingContestPeopleCreateDB.py') as f:
        exec(f.read())
# Run BakingContestEntryCreateDB.py to populate data.
with open('BakingContestEntryCreateDB.py') as f:
    exec(f.read())

# Home route.
@app.route('/')
def home():
    return render_template('home.html')

# Addnew route.
@app.route('/addnew')
def enternew():
    return render_template('enternewuser.html')

# Addrec route.
@app.route('/addrec' , methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        # Get form data.
        nm = request.form['Name']
        ag = request.form['Age']
        pn = request.form['PhoneNumber']
        srl = request.form['SecurityLevel']
        pwd = request.form['Password']

        # List for error messages.
        error_msgs = []

        # Validate and error messages.
        if (len(nm.strip()) == 0):
            error_msgs.append("Can not add record...Name is required.")
        elif not ag.isdigit():
            error_msgs.append("Can not add record...Age must be a valid number.")
        else:
            ag = int(request.form['Age'])
            if(ag < 1 or ag > 120):
                error_msgs.append("Can not add record...Age must be between 1 and 121.")
        if (len(pn.strip()) == 0):
            error_msgs.append("Can not add record...Phone Number is required.")
        if not srl.isdigit():
            error_msgs.append("Can not add record...Security Role Level must be between 1 and 3.")
        else:
            srl = int(srl)
            if srl < 1 or srl > 3:
                error_msgs.append("Can not add record...Security Role Level must be between 1 and 3.")
        if len(pwd.strip()) == 0:
            error_msgs.append("Can not add record...Password is required.")
        elif ' ' in pwd:
            error_msgs.append("Can not add record...Password cannot contain spaces.")

        if error_msgs:
            return render_template("result.html", msg=error_msgs)

        else:
            try:
                with (sql.connect('People.db') as con):
                    cur = con.cursor()

                    cur.execute(
                        "INSERT INTO People (Name, Age, PhNum, SecurityLevel, LoginPassword) "
                        "VALUES (?, ?, ?, ?, ?)", (nm, ag, pn, srl, pwd))

                    con.commit()
                    error_msgs.append("Record successfully added.")

            except:
                con.rollback()
                error_msgs.append("Error in insertion operation.")
            finally:
                con.close()
                return render_template("result.html", msg=error_msgs)

# List route.
@app.route('/list')
def list():
    con = sql.connect('People.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from People")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

# Results route.
@app.route('/results')
def results():
    return 'Results'

# Contestresults route.
@app.route('/contestresults')
def contestresults():
    con = sql.connect('People.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM Entry")

    rows = cur.fetchall()
    return render_template("contestresults.html", rows=rows)

# Run main.
if __name__ == '__main__':
    app.debug = True
    app.run()