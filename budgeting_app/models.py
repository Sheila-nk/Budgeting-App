from datetime import datetime
from budgeting_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    budgets = db.relationship('Budget', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"
   
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deposit_category = db.Column(db.String(20))
    deposit_description = db.Column(db.String(20))
    deposit_amount = db.Column(db.Integer)
    withdraw_category = db.Column(db.String(20))
    withdraw_description = db.Column(db.String(20))
    withdraw_amount = db.Column(db.Integer)
    # add id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Budget('{self.date_posted}', '{self.deposit_category}', '{self.deposit_amount}', '{self.withdraw_category}, '{self.withdraw_amount}')"


"""
To create the database
db.init_app(app)

To initialize database
from budgeting_app import app, db
app.app_context().push()
db.create_all()

To delete the table and content
db.drop_all()
"""