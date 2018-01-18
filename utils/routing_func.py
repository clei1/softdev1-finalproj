from flask import Flask, render_template, request, session, redirect, url_for, flash
import hashlib
from db_func import *

def loggedin():
    print session
    return "user" in session

def vald():
     username = request.form['username']
     password = hashlib.md5(request.form['password'].encode()).hexdigest()
     return validate(username, password)
