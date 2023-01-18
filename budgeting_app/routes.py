from flask import render_template, redirect, request, url_for, flash
from budgeting_app.forms import RegistrationForm, LoginForm, DepositForm, SpendingForm
from budgeting_app.models import User, Budget
from budgeting_app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def index():
    return render_template("public/index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in", 'success')
        return redirect(url_for('login'))
    return render_template("public/register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash("Login Unsuccessful! Please check login information.", 'danger')
    return render_template("public/login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def user_profile():
    return render_template("public/profile.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def user_dashboard():
    depositform = DepositForm()
    spendingform = SpendingForm()

    if depositform.deposit.data and depositform.validate_on_submit():
        budget = Budget(deposit=depositform.deposit.data, user_id=current_user.id)
        db.session.add(budget)
        db.session.commit()
        flash('Deposit added!', 'success')
        return redirect(url_for('user_dashboard'))
         
    if spendingform.category.data and spendingform.amount.data and spendingform.validate_on_submit():
        budget = Budget(category=spendingform.category.data, amount=spendingform.amount.data, user_id=current_user.id)
        db.session.add(budget)
        db.session.commit()
        flash('Withdrawal added!', 'success')
        return redirect(url_for('user_dashboard'))

    headings = ('Date Posted','Deposits', 'Categories', 'Withdrawals')
    result = Budget.query.with_entities(Budget.date_posted, Budget.deposit, Budget.category, Budget.amount)

    return render_template("public/dashboard.html", depositform=depositform, spendingform=spendingform, result=result, headings=headings)
