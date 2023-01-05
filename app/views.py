import sqlite3

from app import app
from flask import render_template, redirect, request, url_for, flash

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/signin")
def sign_in():
    return render_template("public/signin.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    connection = get_db_connection()
    data = connection.execute('SELECT * FROM users').fetchall()
    connection.close()
    
    if request.method == "POST":
        formdata = request.form

        firstname = formdata.get("firstname")
        lastname = formdata.get("lastname")
        email = formdata.get("email")
        password = formdata.get("password")

        print(firstname, lastname, email, password)
        
        return redirect(request.url)
    return render_template("public/register.html", data=data)

@app.route("/profile")
def user_profile():
    return render_template("public/profile.html")

@app.route("/dashboard")
def user_dashboard():
    return render_template("public/dashboard.html")