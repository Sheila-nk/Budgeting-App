from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/signin")
def user_profile():
    return render_template("public/signin.html")