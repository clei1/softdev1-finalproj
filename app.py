from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv, sqlite3, hashlib
from utils.db_func import *

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

@my_app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(url_for('login'))

@my_app.route('/main')
def main():
    return render_template('main.html')

@my_app.route('/login')
def login():
    return render_template('login.html')
    if 'user' in session:
        logged_in()
    else:
        login_form()

@my_app.route('/register')
def register():
    return render_template('register.html')
    if 'user' in session:
        logged_in()
    else:
        register_form()

@my_app.route('/play')
def play():
    return render_template('play.html')

@my_app.route('/create')
def create():
    return render_template('create.html')

@my_app.route('/display')
def display():
    return render_template('display.html')

if __name__ == '__main__':
    my_app.run(debug = True)
