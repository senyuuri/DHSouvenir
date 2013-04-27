# visit.py
from flask import Flask, flash, redirect, render_template,request, session, url_for, g
from functools import wraps
import sqlite3

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Permission denied. You need to login first:(')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out. Bye. :(')
    return redirect (url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again> <'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/register',methods=['GET', 'POST'])
def register():
    pass

@app.route('/main',methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        storelist = None
        db =  connect_db()
        cur = db.execute('''SELECT * FROM store''')
        storelist = [dict(id=row[0],name=row[1],price=row[2],store=row[3]) for row in cur.fetchall()]
        return render_template('main.html', storelist=storelist)
        
    elif request.method == 'POST':
        pass

@app.route('/cart',methods=['GET', 'POST'])
def cart():
    pass

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    pass

@app.route('/mail',methods=['GET', 'POST'])
def mail():
    pass