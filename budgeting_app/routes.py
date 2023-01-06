from flask import render_template, redirect, request, url_for, flash
from budgeting_app.forms import RegistrationForm, LoginForm
from budgeting_app.models import User
from budgeting_app import app

@app.route("/")
@app.route("/home")
def index():
    return render_template("public/index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {}!".format(form.firstname.data), 'success')
        return redirect(url_for('index'))
    return render_template("public/register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash("Successfully logged in!", 'success')
            return redirect(url_for('index'))
        else:
            flash("Login Unsuccessful! Please check login information.", 'danger')
    return render_template("public/login.html", title='Login', form=form)

@app.route("/profile")
def user_profile():
    return render_template("public/profile.html")

@app.route("/dashboard")
def user_dashboard():
    return render_template("public/dashboard.html")