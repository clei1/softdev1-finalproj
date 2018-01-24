from flask import session
from db_func import validate
import hashlib

def loggedin():
    return 'user' in session

def encrypt(pw):
    return hashlib.md5(pw.encode()).hexdigest()

def log(user, pw):
    if validate(user, pw):
        session['user'] = user
        return True
    return False
