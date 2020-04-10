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
import hashlib
import os
import binascii

# initializing the webapp
app = Flask(__name__)

# MySQL Database Connection configurations.
app.config['MYSQL_HOST'] = 'dspinstance.cu7xxjgzv7fk.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'dsp'

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
        cur.execute("SELECT * FROM authentication WHERE user_id =  '{0}' AND "
        "password = '{1}'".format(username, hash_password(password)))
        result = cur.fetchall()
        print(len(result))
        print(hash_password(password))
        if len(result) == 1:
            cur.execute("select * from student")
            result = cur.fetchall()
            return render_template('home.html',data=result)
        cur.close()
        
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
        password = request.form.get("passwd", False)
        ssn = request.form.get("ssn", False)
        department = request.form.get("dpt", False)
        cur = mysql.connection.cursor()
        cur.execute("insert into authentication values('{0}', '{1}')".format(firstname[0:1]+lastname, hash_password(password)))
        print(hash_password(password))
        cur.execute("insert into student(ssn, first_name, last_name, birth_date, email_id, department_id) values('{0}','{1}','{2}','{3}','{4}','{5}')".format(ssn, firstname, lastname, dob, email, department))
        result = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('home.html',data=result)
    return render_template('register.html')

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

# main method
if __name__ == '__main__':
    app.run()