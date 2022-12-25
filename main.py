from flask import Flask, render_template,redirect, url_for, request, session
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import hashlib
import time

import mysql.connector
app = Flask(__name__)
app.config['SECRET_KEY'] = 'januar2021'
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="avgust2021"
    )
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
	if request.method=="GET":
		return render_template('register.html')
	
	username = request.form['username'] 
	email = request.form['email'] 
	password = request.form['password'] 
	confirm = request.form['confirm'] 
	godina_studija = request.form['godina_studija'] 
	jmbg = request.form['jmbg'] 
	
	mc = mydb.cursor()
	mc.execute(f"SELECT * FROM korisnici WHERE username='{username}'")
	rez = mc.fetchall()

	if username=="" or email=="" or password=="" or confirm=="" or godina_studija=="" or jmbg=="":
		return render_template('register.html',odg="Popuni sve forme")
	if len(rez)>0:
		return render_template('register.html',odg="Username postoji")
	if password!=confirm:
		return render_template('register.html',odg="Razlikuju se password")
	if len(jmbg)!=13:
		return render_template('register.html',odg="Nepravilan jmbg")

	mc = mydb.cursor()
	mc.execute(f"INSERT INTO korisnici VALUES (null,'{username}','{password}','{email}',{godina_studija},{jmbg})")
	mydb.commit()

	return redirect(url_for('show_all'))

@app.route('/login',methods=['POST','GET'])
def login():
	if 'username' in session:
		return "Korisnik je ulogovan"
	if request.method=="GET":
		return render_template('login.html')

	username = request.form['username'] 
	password = request.form['password'] 
	
	mc = mydb.cursor()
	mc.execute(f"SELECT * FROM korisnici WHERE username='{username}'")
	rez = mc.fetchall()

	if username=="" or password=="":
		return render_template('login.html',odg="Popuni sve forme")
	if len(rez)==0:
		return render_template('login.html',odg="Nepravilan username")
	if rez[0][2]!=password:
		return render_template('login.html',odg="Nepravilan password")
	
	session['username'] = username
	return redirect(url_for('show_all'))

@app.route('/logout')
def logout():
	if 'username' not in session:
		return redirect(url_for('show_all'))
	session.pop('username',None)
	return redirect(url_for('login'))


@app.route('/show_all')
def show_all():
	if 'username' not in session:
		ulogovan = False
	else:
		ulogovan = True

	mc = mydb.cursor()
	mc.execute(f"SELECT * FROM korisnici")
	rez = mc.fetchall()
	
	return render_template('show_all.html',rez=rez,ulogovan=ulogovan)

@app.route('/show_year/<year>')
def show_year(year):
	if 'username' not in session:
		ulogovan = False
	else:
		ulogovan = True

	mc = mydb.cursor()
	mc.execute(f"SELECT * FROM korisnici WHERE godina='{year}'")
	rez = mc.fetchall()
	
	return render_template('show_all.html',rez=rez,ulogovan=ulogovan)

@app.route('/delete/<username>')
def delete(username):
	if 'username' not in session:
		return redirect(url_for('login'))
	
	mc = mydb.cursor()
	mc.execute(f"DELETE FROM korisnici WHERE username='{username}'")
	mydb.commit()
	
	return redirect(url_for('show_all'))
	
@app.route('/user')
def user():
	if 'username' not in session:
		return redirect(url_for('login'))
	mc = mydb.cursor()
	mc.execute(f"SELECT * FROM korisnici WHERE username='{session['username']}'")
	rez = mc.fetchall()

	return render_template('user.html',rez=rez[0])

@app.route('/update/<username>',methods=['POST'])
def update(username):
	password = request.form['password']
	email = request.form['email']
	godina_studija = request.form['godina_studija']
	
	mc = mydb.cursor()
	mc.execute(f"UPDATE korisnici SET password='{password}', email='{email}', godina='{godina_studija}'")
	mydb.commit()

	return redirect(url_for('show_all'))
if __name__ == '__main__':
	app.run(debug=True)