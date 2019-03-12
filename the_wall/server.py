from flask import Flask, render_template, request, redirect, session, flash, Response
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key="lalaland"
userdb = 'the_wall'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
BIRTHDAY_REGEX = re.compile(r"^\d{4}[-/]\d{2}[-/]\d{2}")
@app.template_filter('duration_elapsed')
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.now()
    diff = now - dt
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default
@app.route('/')
def generate():
	if 'email' not in session:
		session['email'] = ''
		session['first_name'] = ''
		session['last_name'] = ''
		session['password'] = ''
		session['user_id'] = ''
	return render_template("index.html")

@app.route('/validate', methods=['POST'])
def validated():
	mysql = connectToMySQL(userdb)
	if request.form['action'] == 'register':
		session['email'] = request.form['email']
		session['first_name'] = request.form['first_name']
		session['last_name'] = request.form['last_name']
		session['user_id'] = ''
		if len(request.form['first_name']) < 1:
			flash("First Name cannot be blank",'first_name')
		if len(request.form['first_name']) < 2:
			flash("First Name must be at least 2 characters",'first_name')
		elif request.form['first_name'].isalpha() != True:
			flash("First name cannot contain numbers",'first_name')
		if len(request.form['last_name']) < 1:
			flash("Last Name cannot be blank",'last_name')
		if len(request.form['last_name']) < 2:
			flash("Last Name must be at least 2 characters",'last_name')
		elif request.form['last_name'].isalpha() != True:
			flash("First name cannot contain numbers",'last_name')
		if len(request.form['email']) < 1:
			flash("Email cannot be blank",'email')
		if not EMAIL_REGEX.match(request.form['email']):
			flash("Invalid Email Address",'email')
		query = "select * from users where email = %(email)s"
		data = {
			'email':request.form['email']
		}
		emails = mysql.query_db(query,data)
		if emails:
			flash("Email already exists", 'email')
		if len(request.form['password']) < 1:
			flash("Password cannot be blank!", 'password')
		elif len(request.form['password']) < 8:
			flash("Password must be at least 8 characters",'password')
		if not PASSWORD_REGEX.match(request.form['password']):
			flash("Password must contain at least one capital letter and one number",'password')
		if request.form['password'] != request.form['password_confirmation']:
			flash("Passwords must match",'pass_con')
		if '_flashes' in session.keys():
			return redirect('/')
		else:
			mysql = connectToMySQL(userdb)
			query = 'insert into users (first_name, last_name, email, password, created_at, updated_at) values (%(first_name)s, %(last_name)s,%(email)s,%(password)s,now(),now());'
			data = {
				'first_name':request.form['first_name'],
				'last_name' : request.form['last_name'],
				'email' : request.form['email'],
				'password' : bcrypt.generate_password_hash(request.form['password']),
				}
			user_created = mysql.query_db(query,data)
			mysql = connectToMySQL(userdb)
			session['email'] = ''
			session['first_name'] = ''
			session['last_name'] = ''
			session['password'] = ''
			session['user_id'] = ''
			mysql = connectToMySQL(userdb)
			query = 'select * from users where email = %(email)s'
			data = {
				'email':request.form['email']
				}
			checker = mysql.query_db(query,data)
			session['id'] = checker[0]['id']
			session['name'] = checker[0]['first_name']
			session['logged_in'] = True
			return redirect('/success')
	if request.form['action'] == 'login':
		mysql = connectToMySQL(userdb)
		query = 'select * from users where email = %(email)s'
		data = {
			'email':request.form['email']
			}
		checker = mysql.query_db(query,data)
		if checker:
			if bcrypt.check_password_hash(checker[0]['password'], request.form['password']):
				session['id'] = checker[0]['id']
				session['name'] = checker[0]['first_name']
				session['logged_in'] = True
				return redirect('/success')
		flash("You could not be logged in", 'login')
		return redirect('/')
@app.route('/success')
def succeeded():
	mysql = connectToMySQL(userdb)
	query = 'select users.first_name, messages.created_at, messages.message, users.id,messages.id as mid,  messages.sid, user2.first_name as sender_name from users inner join messages on users.id = messages.rid inner join users as user2 on user2.id = messages.sid where users.id = %(id)s;'

	data = {
		'id':session['id']
		}
	left = mysql.query_db(query,data)
	leftcount = len(left)
	mysql = connectToMySQL(userdb)
	query = 'select users.id, users.first_name from users'
	right = mysql.query_db(query)
	mysql = connectToMySQL(userdb)
	query = 'select count(messages.id) as mes_count from messages where messages.sid = %(id)s'
	data = {
		'id':session['id']
	}
	right_tally = mysql.query_db(query,data)
	message_count = right_tally[0]['mes_count']
	return render_template("success.html", left = left, leftcount=leftcount, right = right, rightcount = message_count)
@app.route('/send', methods=['POST'])
def send_message():
	valid = False
	if len(request.form['message']) < 5:
		valid = False
		print(valid)
		temp = request.form['message']
		return render_template('partials/sent.html', valid = valid, temp = temp)
	else:
		valid = True
		print("******************",request.form['message'])
		mysql = connectToMySQL(userdb)
		query = 'insert into messages (message, rid, sid, created_at, updated_at) values (%(message)s, %(rid)s, %(sid)s, now(), now());'
		data = {
			'sid':session['id'],
			'rid':request.form['to_r'],
			'message':request.form['message']
			}
		add = mysql.query_db(query,data)
		print(valid)
		temp = ''
		mysql = connectToMySQL(userdb)
		query = 'select users.first_name, messages.created_at, messages.message, users.id,messages.id as mid,  messages.sid, user2.first_name as sender_name from users inner join messages on users.id = messages.rid inner join users as user2 on user2.id = messages.sid where users.id = %(id)s;'

		data = {
			'id':session['id']
			}
		left = mysql.query_db(query,data)
		leftcount = len(left)
		mysql = connectToMySQL(userdb)
		query = 'select users.id, users.first_name from users'
		right = mysql.query_db(query)
		mysql = connectToMySQL(userdb)
		query = 'select count(messages.id) as mes_count from messages where messages.sid = %(id)s'
		data = {
			'id':session['id']
		}
		right_tally = mysql.query_db(query,data)
		message_count = right_tally[0]['mes_count']
		return render_template('partials/sent.html',valid = valid, temp = temp, message_count = message_count, leftcount=leftcount)
@app.route('/delete', methods=['POST'])
def delete_message():
    mysql = connectToMySQL(userdb)
    query = 'select users.id, users.first_name from users'
    right = mysql.query_db(query)
    mysql = connectToMySQL(userdb)
    query = 'delete from  messages where id = %(mid)s and rid = %(rid)s and sid = %(id)s'
    data = {
    'rid':session['id'],
    'id':request.form['from_r'],
    'mid':request.form['message_id']
    }
    delete = mysql.query_db(query,data)
    return render_template('deleted.html')
@app.route('/logout')
def logger_out():
	session.clear()
	return redirect("/")

if __name__=="__main__":
	app.run(debug=True)
