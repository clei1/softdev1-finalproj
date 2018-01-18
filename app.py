from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils.db_func import *
from utils.routing_func import *
import os, sqlite3, hashlib

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

@my_app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(url_for('login'))

@my_app.route('/login', methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for('main'))
    if request.method == 'POST':
        if vald():
            session['user'] = request.form['username']
            return redirect(url_for('main'))
    return render_template('login.html')

@my_app.route('/register', methods=['GET','POST'])
def register():
    if loggedin():
        return redirect(url_for('main'))
    if request.method == 'POST':
        username = request.form['username']
        if hasUsername(username):
            return render_template('register.html')
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        repeat = hashlib.md5(request.form['repeat'].encode()).hexdigest()
        if password == repeat:
            addUser(username, password)
            return redirect(url_for('login'))
    return render_template('register.html')

@my_app.route('/main', methods=['GET', 'POST'])
def main():
    if 'user' not in session:
        return redirect(url_for('login'))
    c,j,f = [],[],[]
    if "game" in request.form:
        if request.form['game'] == 'current':
            c = getCurrent(session['user'])
            #c = [{"player":"Player", "current":2, "total":4, "players":"Player, hi", "goal":10 }, {"player":"hi", "current":4, "total":8, "players":"Player1, Player2, Player3, hi", "goal":17 }]
        elif request.form['game'] == 'join':
            j = getJoin(session['user'])
            #j = [{"player":"Player2", "current":3, "total":5, "players":"Player2, gdfg, ter", "goal":23 }, {"player":"Player3", "current":1, "total":6, "players":"Player3"}]
        elif request.form['game'] == 'view':
            f = getFinished(session['user'])
            #f = [{"player":"Player5", "current":4, "total":4, "players":"Player5, hi, yt, gf", "goal":14 }, {"player":"Player1", "current":4, "total":4, "players":"Player1, hi, gfe, as", "goal":9 }]
    else:
        c = getCurrent(session['user'])
        #c = [{"player":"Player", "current":2, "total":4, "players":"Player, hi", "goal":10 }, {"player":"hi", "current":4, "total":8, "players":"Player1, Player2, Player3, hi", "goal":17 }]
    return render_template('main.html',
                           current=c,
                           join=j,
                           finished=f)

@my_app.route('/create', methods=['GET','POST'])
def create():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        addGame(session['user'], int(request.form['playerlim']), int(request.form['scorelim']))
        return redirect(url_for('main'))
    return render_template('create.html')

@my_app.route('/play', methods=['GET','POST'])
def play():
    print request.form
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('play.html', playable = True)

@my_app.route('/logout', methods=['GET','POST'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('login'))

if __name__ == '__main__':
    my_app.run(debug = True)

