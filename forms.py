from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField, EmailField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class OrderForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), ])
    address = StringField('Address', validators=[DataRequired()])
    food_item = SelectField('Food Item', choices=[('pizza', 'Pizza'), ('burger', 'Burger'), ('sushi', 'Sushi')], validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired()])
    card_name = StringField('Name on Card', validators=[DataRequired()])
    expiration_date = StringField('Expiration Date', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    submit = SubmitField('Submit')
    