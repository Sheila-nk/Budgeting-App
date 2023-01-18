from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from budgeting_app.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please use another one or log in instead.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class DepositForm(FlaskForm):
    deposit = IntegerField('Deposit', validators=[DataRequired()])
    submit = SubmitField('Add Deposit')

class SpendingForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Spending')

