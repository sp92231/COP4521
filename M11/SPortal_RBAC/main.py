"""
Name: Shanie Portal
Date: 11/05/2024
Assignment: Module 11: Role Based Access Control
Due Date: 11/10/2024
About this project: Develop the database for a small scale real-world applications using third-party Python libraries
discussed in the course.
All work below was performed by Shanie Portal
"""

from flask import Flask, render_template, request, session, flash
import sqlite3 as sql
import os
import secrets

# Create Flask instance.
app = Flask(__name__)
# Set secret key.
app.secret_key = secrets.token_hex(16)
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
def home():  # home page
    # Check if user is not logged in.
    if not session.get('logged_in'):
        # Redirect to login page.
        return render_template('login.html')
    else:
        # Render home page with user's name.
        return render_template('home.html', name=session['name'])

# enternewuser route.
@app.route('/enternewuser')
def enternewuser():
    # Check if the user is not logged in.
    if not session.get('logged_in'):
        # Redirect to login page.
        return render_template('login.html')

    # Check if the user has sufficient security level.
    if session.get('SecurityLevel') < 3:
        abort(404)
    # Render enternewuser.
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

# enternewcontestentry route.
@app.route('/enternewcontestentry', methods=['GET', 'POST'])
def enternewcontestentry():
    # Check if the user is not logged in.
    if not session.get('logged_in'):
        return render_template('login.html')
    if request.method == 'POST':
        return addcontestentry()
    # Render enternewcontestentry.
    return render_template('enternewcontestentry.html')

#addcontestentry route.
@app.route('/addcontestentry', methods=['POST'])
def addcontestentry():
    if request.method == 'POST':
        # Retrieve form data.
        baking_item_name = request.form['NameOfBakingItem']
        num_excellent_votes = request.form['NumExcellentVotes']
        num_ok_votes = request.form['NumOkVotes']
        num_bad_votes = request.form['NumBadVotes']

        # List of error messages.
        error_msgs = []

        # Validate form inputs.
        if len(baking_item_name.strip()) == 0:
            error_msgs.append("Name of the baking item is required.")
        if not num_excellent_votes.isdigit() or int(num_excellent_votes) < 0:
            error_msgs.append("Number of excellent votes must be a non-negative number.")
        if not num_ok_votes.isdigit() or int(num_ok_votes) < 0:
            error_msgs.append("Number of OK votes must be a non-negative number.")
        if not num_bad_votes.isdigit() or int(num_bad_votes) < 0:
            error_msgs.append("Number of bad votes must be a non-negative number.")

        # Check for validation errors.
        if error_msgs:
            return render_template("result.html", msg=error_msgs)

        # If inputs are valid, insert entry.
        try:
            with sql.connect('People.db') as con:
                cur = con.cursor()
                user_id = session.get('user_id')

                # Insert new entry.
                cur.execute(
                    "INSERT INTO Entry (UserId, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (user_id, baking_item_name, num_excellent_votes, num_ok_votes, num_bad_votes)
                )

                con.commit()
                error_msgs.append("Contest entry successfully added.")
        except Exception as e:
            con.rollback()
            error_msgs.append(f"Error in insertion operation: {e}")
        finally:
            con.close()
            return render_template("result.html", msg=error_msgs)

# List route.
@app.route('/list')
def list():
    # Check if user is not logged in.
    if not session.get('logged_in'):
        # Redirect to login page.
        return render_template('login.html')

    # Check if the user has sufficient security level.
    if session.get('SecurityLevel') == 1:
        abort(404)

    con = sql.connect('People.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from People")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


# Route for login.
@app.route('/login', methods=['POST'])
def do_admin_login():
    con = None
    try:
        # Retrieve username and password from form.
        nm = request.form['Username']
        pwd = request.form['Password']

        # Connect to database.
        con = sql.connect('People.db')
        con.row_factory = sql.Row
        cur = con.cursor()

        # Query the database for credentials.
        sql_select_query = """select * from People where Name = ? and LoginPassword = ?"""
        cur.execute(sql_select_query, (nm, pwd))

        row = cur.fetchone()
        if row is not None:
            # Set variables for successful login.
            session['logged_in'] = True
            session['name'] = nm
            session['SecurityLevel'] = int(row['SecurityLevel'])
            session['admin'] = (session['SecurityLevel'] >= 2)
        else:
            # Display an error message for invalid credentials.
            session['logged_in'] = False
            flash('Invalid username and/or password!')
    except Exception as e:
        # Display error message.
        flash(f"Error during login operation: {e}")
    finally:
        if con:
            con.close()
    # Redirect to home.
    return home()

@app.route('/userInfo')
def displayInfo():
    if not session.get('logged_in'):
        # Check if the user is not logged in and redirect to the login page.
        return render_template('login.html')
    else:
        username = session.get('name')

        # Connect to database.
        con = sql.connect('People.db')
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute(
            "SELECT Name, Age, PhNum, SecurityLevel, LoginPassword FROM People WHERE Name=?",
            (username,))

        # Fetch user information.
        rows = cur.fetchall()

        # Return user information.
        return render_template('userInfo.html', rows=rows)

@app.route("/logout")
def logout():
    # Clear session variables to logout.
    session['logged_in'] = False
    session['admin'] = False
    session['name'] = ""

    # Redirect user home.
    return home()

# Results route.
@app.route('/results')
def results():
    return 'Results'

# contestresults route.
from flask import abort

@app.route('/contestresults')
def contestresults():
    # Check if user is not logged in.
    if not session.get('logged_in'):
        # Redirect to login page.
        return render_template('login.html')

    # Check if the user has sufficient security level.
    if session.get('SecurityLevel') < 3:
        abort(404)

    con = sql.connect('People.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM Entry")

    rows = cur.fetchall()
    return render_template("contestresults.html", rows=rows)


@app.route('/mycontestresults')
def mycontestresults():
    # Check if user is not logged in.
    if not session.get('logged_in'):
        # Redirect to login page.
        return render_template('login.html')

    user_name = session['name']

    con = sql.connect('People.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    # Results for the logged-in user.
    cur.execute("""
            SELECT NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes
            FROM Entry
            WHERE UserId = (SELECT UserId FROM People WHERE Name = ?)
        """, (user_name,))

    rows = cur.fetchall()
    return render_template("mycontestresults.html", rows=rows)


# Run main.
if __name__ == '__main__':
    app.debug = True
    app.run()