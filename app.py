"""
File Name : app.py
Date : 03/04/2020
Version : 1.0
Revisions :

This file contains the driver code to run the flask web application. It is responsible for processing the input from the
web page, firing the SQL query and rendering the appropriate output
"""

# importing the required libraries
from flask import Flask, request
from flask import render_template
from flask_mysqldb import MySQL

# initializing the webapp
app = Flask(__name__)

# MySQL Database Connection configurations.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sys'

mysql = MySQL(app)


# The route for the home page. This block of code handles all home-page related operations.
@app.route('/', methods=['GET', 'POST'])
def login():
    """
    This method runs whenever appropriate action happens on the home page. It has the code for processing the input,
    executing the SQL query, fetching the results and rendering them to another web page.

    :return: Appropriate template as per the method (GET/POST)
    """
    if request.method == "POST":

        username = request.form.get("uname", False)
        password = request.form.get("passwd", False)
        cur = mysql.connection.cursor()
        cur.execute("SELECT student_id, mask_SSN(ssn), first_name,last_name,birth_date,email_id,department_id FROM stud"
                    "ent")
        # cur.execute("SELECT ID, FirstName, LastName, mask_SSN(SSN) , Email FROM student WHERE Email =  '{0}' AND "
        # "Password = '{1}'".format(username, password))
        result = cur.fetchall()
        cur.close()
        return render_template('home.html',data=result)
    return render_template('login.html')


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    """
    This method is called when the registration page in the web application is rendered. This method contains code
    for registering a user
    :return: appropriate template as per the method ( GET/POST )
    """
    if request.method == "POST":

        firstname = request.form.get("fname", False)
        lastname = request.form.get("lname", False)
        dob = request.form.get("dob", False)
        email = request.form.get("email", False)
        cur = mysql.connection.cursor()
        cur.execute("select ssn from student where first_name = '%s'" % "'; select true; --")
        result = cur.fetchall()
        cur.close()
        return render_template('home.html',data=result)
    return render_template('register.html')

# main method
if __name__ == '__main__':
    app.run()