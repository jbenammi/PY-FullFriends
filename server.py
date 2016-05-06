from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "I<3SEcretKeys"
mysql = MySQLConnector(app, 'friendsdb')
@app.route('/', methods = ['GET', 'POST'])
def index():
	query = "SELECT * FROM friends"
	fulllist = mysql.query_db(query)
	return render_template('index.html', fulllist = fulllist)

@app.route('/friends', methods=['POST'])
def show():
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at)  VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
	data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'occupation': request.form['occupation']
			}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
	query = "SELECT * FROM friends WHERE id = :id"
	data = {'id': id}
	friend = mysql.query_db(query, data)
	return render_template('edit.html', friend = friend[0])

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation, updated_at = now() WHERE id = :id"
	data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'occupation': request.form['occupation'],
			'id': id
			}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/friends/<id>/delete')
def delete(id):
	query = "DELETE FROM friends WHERE id = :id"
	data = {
			'id': id
			}
	mysql.query_db(query, data)
	return redirect('/')
app.run(debug=True)