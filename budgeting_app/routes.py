from flask import render_template, redirect, request, url_for, flash
from budgeting_app.forms import RegistrationForm, LoginForm, DepositForm, SpendingForm
from budgeting_app.models import User, Budget
from budgeting_app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

deposit_ledger = dict()
withdraw_ledger = dict()

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

    if depositform.deposit_category.data and depositform.deposit_amount.data and depositform.validate_on_submit():
        if depositform.deposit_description.data is None:
            depositform.deposit_description = depositform.deposit_category.data
        budget = Budget(
            deposit_category=depositform.deposit_category.data, 
            deposit_description=depositform.deposit_description.data,
            deposit_amount=depositform.deposit_amount.data,
            user_id=current_user.id
            )
        db.session.add(budget)
        db.session.commit()
        flash('Deposit added!', 'success')
        if deposit_ledger.get(depositform.deposit_category.data, 0):
            value = deposit_ledger.get(depositform.deposit_category.data)
            deposit_ledger[depositform.deposit_category.data] = int(value) + int(depositform.deposit_amount.data)
        else:
            deposit_ledger[depositform.deposit_category.data] = int(depositform.deposit_amount.data)
        return redirect(url_for('user_dashboard'))

       
    if spendingform.withdraw_category.data and spendingform.withdraw_amount.data and spendingform.validate_on_submit():
        if spendingform.withdraw_description.data is None:
            spendingform.withdraw_description = spendingform.withdraw_category.data
        budget = Budget(
            withdraw_category=spendingform.withdraw_category.data,
            withdraw_description=spendingform.withdraw_description.data,
            withdraw_amount=spendingform.withdraw_amount.data, 
            user_id=current_user.id
            )
        db.session.add(budget)
        db.session.commit()
        flash('Withdrawal added!', 'success')
        if withdraw_ledger.get(spendingform.withdraw_category.data, 0):
            value = withdraw_ledger.get(spendingform.withdraw_category.data)
            withdraw_ledger[spendingform.withdraw_category.data] = int(value) + int(spendingform.withdraw_amount.data)
        else:
            withdraw_ledger[spendingform.withdraw_category.data] = int(spendingform.withdraw_amount.data)
        return redirect(url_for('user_dashboard'))

    headings = ('Deposit', 'Amount', 'Withdrawal', 'Amount')
    result = Budget.query.filter_by(user_id=current_user.id).with_entities(Budget.deposit_category, Budget.deposit_amount, Budget.withdraw_category, Budget.withdraw_amount)
 
    return render_template("public/dashboard.html", depositform=depositform, spendingform=spendingform, result=result, headings=headings, deposit_ledger=deposit_ledger, withdraw_ledger=withdraw_ledger) 

@app.route("/transactions")
@login_required
def user_transactions():
    headings = ('Date Posted','Income', 'Description', 'Amount', 'Expense', 'Description', 'Amount')
    result = Budget.query.filter_by(user_id=current_user.id).with_entities(Budget.date_posted, Budget.deposit_category, Budget.deposit_description, Budget.deposit_amount, Budget.withdraw_category, Budget.withdraw_description, Budget.withdraw_amount)

    return render_template("public/transactions.html", result=result, headings=headings)

class TrackTransactions:
    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = list()

    def deposit(self, category_name, amount):
        self.ledger.append({"category": category_name, "amount": amount})

    def withdraw(self, category_name, amount):
        self.ledger.append({"category": category_name, "amount": -amount})

    def get_balance(self):
        current_balance = 0
        for entry in self.ledger:
            current_balance += entry["amount"]
        return current_balance
