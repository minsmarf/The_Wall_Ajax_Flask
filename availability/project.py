#   Warren Haskins
#   
#   


from flask import Flask, render_template, request, session, flash, redirect
from flask_bcrypt import Bcrypt

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#import getpass
#passw = getpass.getpass()
# passfile = open('/Users/warren/passfile.txt')
# passdata = passfile.read()
# passw = passdata.split('\n')[0]
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'hi there'
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
        user = 'root',
        password = 'root',
        db = db,
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor,
        autocommit = True)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
reg_info = {
    'email': 'Email',
    'password': 'Password',
    'confpass': 'Confirm Password',
    'first_name': 'First Name',
    'last_name': 'Last Name',
}
log_info = {
    'email': 'Email',
    'passw': 'Password'
}

@app.route('/')
def default():
    mysql = connectToMySQL('the_wall')	        # call the function, passing in the name of our db
    print(reg_info)
    return render_template('index.html', reg_fields = reg_info, log_fields = log_info)
@app.route('/register', methods=['post'])
def register():
    is_valid = True
    for field in reg_info:
        if len(request.form[field]) < 3:
            flash('Must be at least three characters', field)
            is_valid = False
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Please enter a valid email address', 'email')
        is_valid = False
    check_unique_email = connectToMySQL('the_wall')
    is_unique_email = check_unique_email.query_db("select * from users where email = '%s'" %request.form['email'])
    if len(is_unique_email) > 0:
        flash('Email already registered', 'email')
        is_valid = False
    if request.form['passw'] != request.form['confpass']:
        flash('Passwords do not match')
        is_valid = False
    if not is_valid:
        return redirect('/')
    data = {}
    post_registration = connectToMySQL('the_wall')
    query = "insert into users ("
    column_str = ""
    info_str = ""
    for item in reg_info:
        if item != 'confpass':
            if item == 'passw':
                data[item] = bcrypt.generate_password_hash(request.form[item])
            else:
                data[item] = request.form[item]
            column_str += "%s, " % item
            info_str += "%("
            info_str += "%s)s, " % item
    query += column_str + "date_created, date_modified) values (" + info_str + " now(), now())"
    session['id'] = post_registration.query_db(query, data)
    
        
    return redirect('/success')
@app.route('/login', methods=['post'])
def verify():
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Please enter a valid email address', 'email')
        is_valid = False
    if len(request.form['passw']) < 3:
        flash('password too short')
        is_valid = False
    mysql = connectToMySQL('the_wall')
    
    pass_hash = mysql.query_db("select passw, id from users where email = '%s'" % request.form['email'])
    if len(pass_hash) < 1:
        flash('User not found')
        return redirect('/')
    print('!' *500)
    print(pass_hash)
    print(pass_hash)
    if not bcrypt.check_password_hash(pass_hash[0]['passw'], request.form['passw']):
        flash('Credentials do not match')
        is_valid = False
    if not is_valid:
        return redirect('/')
    session['uid'] = pass_hash[0]['id']
    flash('You are logged in as: %s' % request.form['email'])
    return redirect('/success')
@app.route('/success')
def success():
    if not session:
        return redirect('/')
    return render_template('success.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/email', methods=['post'])
def validate_email():
    print(request.form['email'])
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Please enter a valid email address', 'email')
        success = 'error'

        return render_template('partials/valid.html', success = success)
    check_unique_email = connectToMySQL('the_wall')
    is_unique_email = check_unique_email.query_db("select * from users where email = '%s'" %request.form['email'])
    if len(is_unique_email) > 0:
        flash('Email already registered')
        success = 'error'
        return render_template('partials/valid.html', success = success)
    success = 'success'
    flash('valid email')
    return render_template('partials/valid.html', success = success)
if __name__ == "__main__":
    app.run(debug=True)