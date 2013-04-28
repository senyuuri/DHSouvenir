#main.py alpha0.2
import os
from flask import Flask, flash, redirect, render_template,request, session, url_for, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager,login_user, logout_user, current_user, login_required
from flask.ext.openid import OpenID

from model import *
from forms import *
from config import basedir

#flask init
app = Flask(__name__)
app.config.from_object('config')

#sqlalchemy init
db = SQLAlchemy(app)

#login init
lm = LoginManager()
lm.setup_app(app)
#flask-login redirect address
lm.login_view = 'login'

#openid init
oid = OpenID(app, os.path.join(basedir, 'tmp'))

#required by flask-login
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('main'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	return render_template('login.html', 
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		redirect(url_for('login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(username = nickname, email = resp.email, role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('main'))

@app.route('/')
def welcome():
	return "welcome!"

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('welcome'))

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username = username).first()
	if user == None:
		flash('User not exist:'+username+'!')
		return redirect(url_for('main'))
	posts = [
		{ 'author': user, 'body': 'Test post #1' },
		{ 'author': user, 'body': 'Test post #2' }
	]
	return render_template('profile.html',
		user = user,
		posts = posts)

@app.route('/main',methods=['GET', 'POST'])
@login_required
def main():
	user = g.user
	if request.method == 'POST':
		#rdata = request.form.getlist('rorder')
		rdata = request.form.getlist('rorder')
		ss = Store.query.all()
		if not Uorder.query.filter(Uorder.uid==user.uid).first():
			#construct raw list with index
			i = 1
			raw = []
			for r in rdata:
				t = [i, r]
				i += 1
				raw.append(t)
			#add order to db & modify store state
			for r in raw:
				uid = user.uid
				pid = int(r[0])
				num = int(r[1])
				u = Uorder(uid=uid,pid=pid,num=num)
				db.session.add(u)
			
			for s in ss:
				s.number = s.number - int(rdata[int(s.pid)-1])
				db.session.merge(s)
			db.session.commit()
			#update order to db
			temp=[]
			result = Uorder.query.filter(Uorder.uid==user.uid).all()
			for r in result:
				r.num = r.num + int(rdata[int(r.pid)-1])
				db.session.merge(r)
			for s in ss:
				s.number = s.number - int(rdata[int(s.pid)-1])
				db.session.merge(s)
			db.session.commit()

		return redirect(url_for('cart'))

	user = g.user
	storelist = Store.query.all()
	return render_template('main.html', user=user, storelist=storelist)

@app.route('/cart',methods=['GET', 'POST'])
def cart():
	user = g.user
	return render_template('cart.html')

@app.route('/mail',methods=['GET', 'POST'])
def mail():
	pass

if __name__ == '__main__':
	app.run(host="localhost",port=8888,debug=True)