from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, EqualTo, InputRequired, NumberRange


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class WriteForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    date = IntegerField("Release Year", default=date.today().year, validators=[DataRequired(), NumberRange(min=0, max=date.today().year, message="Year has to be valid.")])
    text = TextAreaField("Text", validators=[DataRequired()])
    rating = IntegerField("Rating", default=50, validators=[InputRequired(), NumberRange(min=0, max=100, message="Number has to be between 0 and 100.")])
    submit = SubmitField("Publish")
